import discord
import asyncio
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
ROLE_ID = int(os.getenv('ROLE_ID'))
MESSAGE_INTERVAL = int(os.getenv('MESSAGE_INTERVAL'))  # Interval in seconds
SEND_MESSAGE = os.getenv('SEND_MESSAGE')  # Message to send
MESSAGE_DELAY = int(os.getenv('MESSAGE_DELAY', 1))  # Delay in seconds between messages

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    send_message.start()

@tasks.loop(seconds=MESSAGE_INTERVAL)
async def send_message():
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if not guild:
        print("Guild not found.")
        return

    role = discord.utils.get(guild.roles, id=ROLE_ID)
    if not role:
        print("Role not found.")
        return

    for member in role.members:
        try:
            await member.send(f"<@{member.id}> {SEND_MESSAGE}")
            print(f"Sent message to {member.name}")
        except discord.Forbidden:
            print(f"Cannot send message to {member.name}: Forbidden")
        except discord.HTTPException as e:
            print(f"Cannot send message to {member.name}: HTTPException - {e}")
        except Exception as e:
            print(f"Cannot send message to {member.name}: {e}")
        await asyncio.sleep(MESSAGE_DELAY)  # Delay between sending messages

@send_message.before_loop
async def before_send_message():
    await bot.wait_until_ready()

bot.run(TOKEN)
