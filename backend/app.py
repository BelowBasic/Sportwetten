import asyncio
import requests
import redis.asyncio as redis
import pika
import datetime
import logging


async def init_results(cache):
    """Reads all Results from opelnliigadb.de for the Bundeliga from the current year Back until there is no data available and saves the amount of wins into redis using the alphabetical ordered Teams as key eg "1. FC Nürnberg:Zwickauer FC"  team_a """
    print("Backend Running")
    year = datetime.datetime.now().year
    game_data_api_url = "https://api.openligadb.de/getmatchdata/bl1/"
    x = year
    while True:
        print(x)
        resp = requests.get( game_data_api_url+str(x))
        games = resp.json()
        if len(games)<= 0 and year != x:
            break
        for game in games:
            team1_name = game.get("team1",{}).get("teamName")
            team2_name = game.get("team2",{}).get("teamName")
            print(team1_name)
            results = game.get("matchResults",[])
            #print(results)
            if len(results)>0:          
                endresult = results[-1]
                team1_points = endresult.get("pointsTeam1")
                team2_points = endresult.get("pointsTeam2")
                team_names = sorted([team1_name,team2_name])
                key = team_names[0]+":"+team_names[1]
                teams = {team1_name:team1_points,team2_name:team2_points}
                teams = dict(sorted(teams.items()))
                result_data = await cache.hgetall(key)
                print(key)
                print(result_data)
                
                if not isinstance(result_data,dict):
                    result_data = {
                    b'team_a_wins': 0,
                    b'team_b_wins': 0,
                    b'tie': 0,
                    }
                else:
                    print(result_data)
                if list(teams.values())[0]> list(teams.values())[1]:
                    result_data.update({b'team_a_wins': int(result_data.get(b'team_a_wins',0)) +1 } )
                else: 
                    if list(teams.values())[0] == list(teams.values())[1]:
                        result_data.update({b'tie': int(result_data.get(b'tie',0)) +1 } )
                    else: 
                        result_data.update({b'team_b_wins': int(result_data.get(b'team_b_wins',0)) +1 } )
                await cache.hset(key, mapping=result_data)
            else:
                break   
        x=x-1
    print("init finished")
    
async def get_frequency(cache,team_a,team_b,bet):
    """gets the result statistics from redis and returns a multiplier bet 'a' menas a win 'b' team b win and 't' tie """
    team_names = sorted([winner,loser])
    key = team_names[0]+":"+team_names[1]
    try:
         results = await cache.get(key)
    except redis.exceptions.ConnectionError as exc:
    if team_a == team_names[0]
        team_a_results = int(results.get(b'team_a_wins',0))
        team_b_results = int(results.get(b'team_b_wins',0))
    else:
        team_b_results = int(results.get(b'team_a_wins',0))
        team_a_results = int(results.get(b'team_b_wins',0))
    tie = int(results.get(b'tie',0))
    game_total =  team_a_results + team_b_results + tie
    match bet:
    case 'a':
        winner = team_a
    case 'b':
        winner = team_b
    case 't':
        return game_total/tie
    case _:
        logging.error("Bet key invalid")
        return False
    return game_total/winner

def return_result(winner,loser,result)
   

async def consume_queues(channel):
    channel.basic_consume(queue='frequency',
                      auto_ack=True,
                      on_message_callback=get_frequency)
    channel.basic_consume(queue='games',
                      auto_ack=True,
                      on_message_callback=get_game)
    
def main():
    redis_pool = redis.ConnectionPool.from_url("redis://redis")
    cache_games(datetime.datetime.now().year)
    #connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672,
    #                                   '/',))
    #channel = connection.channel()
    connection_1 = redis.Redis(connection_pool=redis_pool)
    asyncio.run(calculate_frequency(connection_1))

    #consume_queues(channel)
    #asyncio.run(init_redis_pool())

async def init_redis_pool():
        while True:
            events = await pool.xread(['wins_stream'], latest_ids=[last_id], timeout=0, count=10)
            # Process each event by calling `add_new_win`
            for _, e_id, e in events:
                winner = e['winner']
                await add_new_win(pool, winner)
                last_id = e_id
            
if __name__=="__main__": 
    main() 

