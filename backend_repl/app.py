import asyncio
import requests
import redis.asyncio as redis
import datetime

#  flask imports for api
from flask import Flask

# flask app init
app = Flask(__name__)

# api routes for the frontend
# dummy route for testing connection
@app.route('/')
def hello_world():
    return 'Hello, World!'

def start_flask():
    app.run(debug=True, port=5001, host='0.0.0.0')


async def init_results(cache):
    """Reads all Results from opelnliigadb.de for the Bundeliga from the current year Back until there is no data available and saves the amount of wins into redis using the alphabetical ordered Teams as key eg "1. FC Nürnberg:Zwickauer FC"  team_a """
    print("Backend Running")
    year = datetime.datetime.now().year
    game_data_api_url = "https://api.openligadb.de/getmatchdata/bl1/"
    x = year
    while True:
        print(x)
        resp = requests.get(game_data_api_url + str(x))
        games = resp.json()
        if len(games) <= 0 and year != x:
            break
        for game in games:
            team1_name = game.get("team1", {}).get("teamName")
            team2_name = game.get("team2", {}).get("teamName")
            print(team1_name)
            results = game.get("matchResults", [])
            #print(results)
            if len(results) > 0:
                endresult = results[-1]
                team1_points = endresult.get("pointsTeam1")
                team2_points = endresult.get("pointsTeam2")
                team_names = sorted([team1_name, team2_name])
                key = team_names[0] + ":" + team_names[1]
                teams = {team1_name: team1_points, team2_name: team2_points}
                teams = dict(sorted(teams.items()))
                result_data = await cache.hgetall(key)
                print(key)
                print(result_data)

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
        x = x - 1
    print("init finished")


def main():
    redis_pool = redis.ConnectionPool.from_url("redis://redis")
    connection_1 = redis.Redis(connection_pool=redis_pool)
    asyncio.run(init_results(connection_1))
    start_flask()


if __name__ == "__main__":
    main()
