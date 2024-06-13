# import asyncio
import requests
import redis as redis
import datetime
import logging
import random

from flask import Flask
from flask import request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
redis_pool = None

@app.route("/bet",methods=['POST'])
def bet():
    team_a = request.json.get("team_a")
    team_b = request.json.get("team_b")
    stake = request.json.get("stake")
    bet = request.json.get("bet")
    freq = get_frequency(team_a,team_b,bet)
    num = random.randint(0,100)
    if round((1/freq)*100) < num:
        multiplier = 1
    else:
        multiplier = 0

    return {"result": freq*stake*multiplier}
    
@app.route("/game_list",methods=['GET'])
def game_list():
    return get_current_season()
    

def get_current_season():
    year = datetime.datetime.now().year
    game_data_api_url = "https://api.openligadb.de/getmatchdata/bl1/"
    x = year
    response_dict = []
    game_list = []
    while True:
        logging.debug(x)
        resp = requests.get(game_data_api_url + str(x))
        games = resp.json()
        if len(games) <= 0:
            logging.debug(x)
            x = x - 1
        else:
            for game in games:
                if isinstance(game,list):
                    logging.debug("Hä??")
                    break
                logging.debug(game)
                team1_name = game.get("team1", {}).get("teamName")
                team2_name = game.get("team2", {}).get("teamName")
                team_names = sorted([team1_name, team2_name])
                if team_names in game_list:
                    leg = "return"
                else: 
                    leg = "first"
                multiplier_win_a = get_frequency( team1_name,team2_name , "a")
                multiplier_win_b = get_frequency( team1_name,team2_name , "b")
                multiplier_tie = get_frequency( team1_name,team2_name , "t")
                games.append(team_names)
                response_dict.append({
                    "team_a": team_names[0],
                    "team_b": team_names[1],
                    "multiplier_win_a": multiplier_win_a,
                    "multiplier_win_b": multiplier_win_b,
                    "multiplier_tie": multiplier_tie,
                    "leg" : leg  })
            return response_dict


def start_flask():
    app.run(debug=True, port=5000, host="0.0.0.0")


def init_results():
    """Reads all Results from openligadb.de for the Bundesliga from the current year Back until there is no
     data available and saves the amount of wins into redis using the alphabetical ordered Teams as key
     eg "1. FC Nürnberg:Zwickauer FC"  team_a """
    cache = redis.Redis(connection_pool=redis_pool)
    logging.info("Backend Running")
    init_status = cache.get("init_status")
    if str(init_status) == "finished":
        logging.info("init already ran ")
        return 
    year = datetime.datetime.now().year
    game_data_api_url = "https://api.openligadb.de/getmatchdata/bl1/"
    x = year
    i = 0 
    while True:
        logging.info(f"Processing year: {x}")
        try:
            resp = requests.get(game_data_api_url+str(x))
            if resp.status_code != 200:
                logging.error(f"Failed to fetch data for year {x}, status code: {resp.status_code}")
                break
            games = resp.json()
        except Exception as e:
            logging.error(f"Error fetching data for year {x}: {e}")
            break

        if len(games) <= 0 and year != x:
            break

        for game in games:
            try:
                team1_name = game.get("team1", {}).get("teamName")
                team2_name = game.get("team2", {}).get("teamName")
                logging.info(f"Processing game: {team1_name} vs {team2_name}")
                results = game.get("matchResults", [])
            # check if a result is already there (the game has concluded)
                if len(results) > 0:
                    endresult = results[-1]
                    team1_points = endresult.get("pointsTeam1")
                    team2_points = endresult.get("pointsTeam2")
                    team_names = sorted([team1_name, team2_name])
                    key = team_names[0]+":"+team_names[1]
                    teams = {team1_name: team1_points, team2_name: team2_points}
                    teams = dict(sorted(teams.items()))
                    result_data = await cache.hgetall(key)
                    logging.info(f"Processing game: {team1_name} vs {team2_name}")
                # If team combination does not exists intialize result_data with a dict with 0 wins and ties
                    if not isinstance(result_data, dict):
                        result_data = {
                            b'team_a_wins': 0,
                            b'team_b_wins': 0,
                            b'tie': 0,
                        }
                    else:
                        print(result_data)
                    if list(teams.values())[0] > list(teams.values())[1]:
                        result_data.update({b'team_a_wins': int(result_data.get(b'team_a_wins', 0)) + 1})
                    else:
                        if list(teams.values())[0] == list(teams.values())[1]:
                            result_data.update({b'tie': int(result_data.get(b'tie', 0)) + 1})
                        else:
                            result_data.update({b'team_b_wins': int(result_data.get(b'team_b_wins', 0)) + 1})
                    await cache.hset(key, mapping=result_data)
                else:
                    break
            except Exception as e:
                logging.error(f"Error processing game data: {e}")
                continue

        x = x-1
    logging.info("init finished")


async def get_frequency(cache, team_a, team_b, bet):
    """gets the result statistics from redis and returns a multiplier bet
    'a' means a wins, 'b' team b wins and 't' means tie """
    team_names = sorted([team_a, team_b])
    key = team_names[0] + ":" + team_names[1]
    try:
        results = await cache.get(key)
        if not results:
            logging.error(f"No data found for key: {key}")
            return False
    except redis.exceptions.ConnectionError as exc:
        logging.error(f"Redis connection error: {exc}")
        return False
    if team_a == team_names[0]:
        team_a_results = int(results.get(b"team_a_wins", 1))
        team_b_results = int(results.get(b"team_b_wins", 1))
    else:
        team_b_results = int(results.get(b"team_a_wins", 1))
        team_a_results = int(results.get(b"team_b_wins", 1))
    tie = int(results.get(b"tie", 1))
    game_total = team_a_results + team_b_results + tie
    match bet:
        case "a":
            winner = team_a_results
        case "b":
            winner = team_b_results
        case "t":
            return game_total / tie
        case _:
            logging.error("Bet key invalid")
            return False
    return game_total / winner




def main():
    global redis_pool
    redis_pool = redis.ConnectionPool.from_url("redis://redis")
    init_results()
    start_flask()

  


if __name__ == "__main__":
    main()
