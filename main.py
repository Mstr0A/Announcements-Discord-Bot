import discord
from discord.ext import commands, tasks
import aiohttp
import pymysql.cursors
import asyncio
import os
import json
import sys

sys.path.insert(0, os.path.dirname(__file__))

intents = discord.Intents.default()
intents.members = True
intents = discord.Intents().all()

client = commands.Bot(command_prefix='/', intents=intents)

hostname = 'localhost'
username = 'root'
password = ''
database = ''

TOKEN = "INSERT TOKEN"

new_challenges = set()

new_chall_data = []
new_chall_file = "new_chall.json"

if os.path.exists(new_chall_file):
    os.remove(new_chall_file)

with open(new_chall_file, "w") as file:
    json.dump(new_chall_data, file)


def create_connection():
    try:
        connection = pymysql.connect(
            host=hostname,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


async def get_new_chall():
    loop = asyncio.get_event_loop()
    connection = await loop.run_in_executor(None, create_connection)

    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, adminName, CHname, CHpoint, CHcategory, CHlevel, CHstatus FROM challenges"
                cursor.execute(sql)
                new_chall_entries = cursor.fetchall()
                
                for entery in new_chall_entries:
                    new_chall_entry = {
                        'id': entery['id'],
                        'adminName': entery['adminName'],
                        'challName': entery['CHname'],
                        'points': entery['CHpoint'],
                        'category': entery['CHcategory'],
                        'level': entery['CHlevel'],
                        'status': entery['CHstatus']
                    }
                    new_chall_data.append(new_chall_entry)

                return new_chall_data
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally: 
            connection.close()


emojis = ['👽','🔥']


@tasks.loop(seconds=60)
async def check_new_chall():
    general_channel_id = 123
    admin_channel_id = 456

    new_chall_entries = await get_new_chall()
    
    general_channel = client.get_channel(general_channel_id)
    admin_channel = client.get_channel(admin_channel_id)

    if new_chall_entries:
        for entry in new_chall_entries:
            challenge_id = entry['id']

            if challenge_id not in new_challenges:
                admin_name = entry['adminName']
                challenge_name = entry['challName']
                challenge_level = entry['level']
                challenge_points = entry['points']
                challenge_category = entry['category']
                challenge_status = entry['status']


                admin_message = f"**{admin_name}** has posted a new challenge, info: \n**Challenge name:** {challenge_name}\n**Challenge category:** {challenge_category}\n**Challenge level:** {challenge_level}\n**Challenge points:** {challenge_points}\n**Challenge Status:** {challenge_status}"
                
                admin_embed = discord.Embed(
                    description=admin_message,
                    color=0xFF5733
                )
                
                general_message = f"**{admin_name}** has posted a new challenge, info: \n**Challenge name:** {challenge_name}\n**Challenge category:** {challenge_category}\n**Challenge level:** {challenge_level}\n**Challenge points:** {challenge_points}"
                
                general_embed = discord.Embed(
                    description=general_message,
                    color=0xFF5733
                )

                admin_new_chall_message = await admin_channel.send(embed=admin_embed)

                for emoji in emojis:
                    await admin_new_chall_message.add_reaction(emoji)
                
                if challenge_status == 'ON':
                    general_new_chall_message = await general_channel.send(embed=general_embed)

                    for emoji in emojis:
                        await general_new_chall_message.add_reaction(emoji)

                new_challenges.add(challenge_id)

                with open("new_chall.json", "w") as file:
                    json.dump(new_chall_data, file)


@client.event
async def on_ready():
    print("Bot is ready.")
    check_new_chall.start()


async def start_bot():
    while True:
        try:
            await client.start(TOKEN)
        except aiohttp.ClientConnectorError:
            print("Connection failed, retrying in 5 seconds...")
            await asyncio.sleep(5)
        except KeyboardInterrupt:
            print("Bot stopped by the user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)


async def run_bot_and_web():
    await start_bot()

    app = web.Application()
    app.router.add_route('GET', '/', wsgi_app)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(run_bot_and_web())