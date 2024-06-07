import time
import asyncio
import requests
import aioredis
import pika
import datetime

async def cache_games(year):
    cache = redis.Redis(host='redis', port=6379)
    game_data_api_url = "https://api.openligadb.de/getmatchdata/bl1/"
    resp = requests.get( game_data_api_url+str(year) , params=params)
    games = resp.json()
    for game in games:
        game.get("")

async def get_games():
        while True:
            try:
                return cache.get(body)
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
    
def calculate_frequency():
    """Reads"""
    year = Datetime.now().year
    cache = redis.Redis(host='redis', port=6379)
    game_data_api_url = "https://api.openligadb.de/getmatchdata/bl1/"
    x =year
    while True:

        resp = requests.get( game_data_api_url+str(year))
        games = resp.json()
        if len(games)<= 0 and year != x:
            break
        for game in games:
            team1_name = game.get("team1",{}).get("teamName")
            team2_name = game.get("team2",{}).get("teamName") 
            results = game.get("matchResults",None)
            if results is not None:
                endresult = results[-1]
                team1_points = endresult.get("pointsTeam1")
                team2_points = endresult.get("pointsTeam2")
                cache.
            else:
                break   
        x=x-1
def get_frequency(ch, method, properties, body):
        while True:
            try:
                return cache.get(body)
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
   

def consume_queues():
    channel.basic_consume(queue='frequency',
                      auto_ack=True,
                      on_message_callback=get_frequency)
    channel.basic_consume(queue='games',
                      auto_ack=True,
                      on_message_callback=get_game_day)
    
def main():
    redis_pool = await aioredis.create_redis_pool('redis://redis', encoding='utf8')
    cache_games(Datetime.now().year)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    calculate_frequency(cache)
    consume_queues(channel)
    while True:
        events = await pool.xread(['wins_stream'], latest_ids=[last_id], timeout=0, count=10)
        # Process each event by calling `add_new_win`
        for _, e_id, e in events:
            winner = e['winner']
            await add_new_win(pool, winner)
            last_id = e_id