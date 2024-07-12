import discord
from discord.ext import commands, tasks
from pubg_api import get_pubg_data
from database_operations import add_player, update_player, delete_player, get_player, get_leaderboard, get_all_players, update_player_data, init_db
from image_utils import create_leaderboard_image
import os
from dotenv import load_dotenv
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize the database
init_db()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
scheduler = AsyncIOScheduler()
players_to_update = []
leaderboard_channel_id = None  # 리더보드 채널 ID 저장

# 채널 ID를 파일에 저장하는 함수
def save_channel_id(channel_id, filename='channel_id.json'):
    with open(filename, 'w') as file:
        json.dump({'channel_id': channel_id}, file)

# 파일에서 채널 ID를 로드하는 함수
def load_channel_id(filename='channel_id.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('channel_id')
    except (FileNotFoundError, json.JSONDecodeError):
        return None

@bot.event
async def on_ready():
    global players_to_update, leaderboard_channel_id
    print(f'{bot.user.name} has connected to Discord!')
    players_to_update = get_all_players()
    leaderboard_channel_id = load_channel_id()  # 파일에서 채널 ID 로드

    # 매 시간마다 리더보드를 게시하는 작업을 예약합니다.
    scheduler.add_job(post_leaderboard, 'interval', hours=1)
    scheduler.start()

    update_data.start()

@bot.command(name='채널설정')
async def set_channel(ctx, channel: discord.TextChannel):
    global leaderboard_channel_id
    leaderboard_channel_id = channel.id
    save_channel_id(channel.id)  # 채널 ID 파일에 저장
    await ctx.send(f'리더보드 채널이 {channel.mention}으로 설정되었습니다.')

@set_channel.error
async def set_channel_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('채널을 지정해야 합니다. 예: !채널설정 #your-leaderboard-channel')
    else:
        await ctx.send(f'오류가 발생했습니다: {error}')

@bot.command(name='추가')
async def add(ctx, player_name: str, clan: str):
    rank_points = get_pubg_data(player_name)
    if rank_points is not None:
        add_player(player_name, rank_points, clan)
        await ctx.send(f'{player_name}를 랭크 포인트 {rank_points}, 클랜 {clan}로 추가했습니다.')
        print(f"Added player {player_name} with rank points {rank_points} and clan {clan}")
    else:
        await ctx.send('PUBG API로부터 데이터를 가져오는 데 실패했습니다.')
        print(f"Failed to fetch data for player {player_name}")

@bot.command(name='수정')
async def update(ctx, player_name: str, new_points: int, clan: str):
    if update_player(player_name, new_points, clan):
        await ctx.send(f'{player_name}의 정보를 랭크 포인트 {new_points}, 클랜 {clan}로 갱신했습니다.')
        print(f"Player {player_name} updated with rank points {new_points} and clan {clan}")
    else:
        await ctx.send(f'{player_name}의 데이터를 찾을 수 없습니다.')

@bot.command(name='삭제')
async def delete(ctx, player_name: str):
    if delete_player(player_name):
        await ctx.send(f'{player_name}의 정보를 데이터베이스에서 삭제했습니다.')
        print(f"Player {player_name} deleted")
    else:
        await ctx.send(f'{player_name}의 데이터를 찾을 수 없습니다.')

@bot.command(name='조회')
async def get(ctx, player_name: str):
    player = get_player(player_name)
    if player:
        await ctx.send(f'플레이어: {player[0]}, 랭크 포인트 {player[1]}, 클랜 {player[2]}')
    else:
        await ctx.send('플레이어를 찾을 수 없습니다.')

@bot.command(name='리더보드')
async def leaderboard(ctx):
    players = get_leaderboard()
    print(players)  # 디버그 출력 추가
    if players:
        leaderboard_image = create_leaderboard_image(players)
        leaderboard_image.save("leaderboard.png")
        await ctx.send(file=discord.File("leaderboard.png"))
    else:
        await ctx.send("플레이어 데이터가 없습니다.")

@tasks.loop(minutes=3)
async def update_data():
    global players_to_update
    if players_to_update:
        player_name = players_to_update.pop(0)
        rank_points = get_pubg_data(player_name)
        if rank_points is not None:
            update_player_data(player_name, rank_points)
            print(f'Updated {player_name}: Rank Points {rank_points}')
        else:
            print(f'Failed to update data for {player_name}')
        players_to_update.append(player_name)

async def post_leaderboard():
    global leaderboard_channel_id
    if leaderboard_channel_id is None:
        print("Error: The leaderboard channel has not been set.")
        return

    channel = bot.get_channel(leaderboard_channel_id)
    if channel and isinstance(channel, discord.TextChannel):
        players = get_leaderboard()
        if players:
            leaderboard_image = create_leaderboard_image(players)
            leaderboard_image.save("leaderboard.png")
            await channel.send(file=discord.File("leaderboard.png"))
        else:
            await channel.send("플레이어 데이터가 없습니다.")
    else:
        print("Error: The channel is not a TextChannel or does not exist.")

# Get the Discord bot token from the environment variable
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if DISCORD_BOT_TOKEN is None:
    raise ValueError("No Discord bot token found. Please set the DISCORD_BOT_TOKEN environment variable.")

bot.run(DISCORD_BOT_TOKEN)
