# from lib.database import DBConnection
import discord
from discord.ext import commands
import os
# from model import image


TOKEN = os.getenv("TOKEN")
GUILDS = os.getenv("GUILDS")
intents = discord.Intents.default()

bot = commands.Bot(
    debug_guilds=[int(v) for v in GUILDS.split(",")],
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Bot名:{bot.user} On ready!!")


@bot.slash_command()
async def test(ctx: discord.ApplicationContext):
    await ctx.respond("test")


bot.load_extensions(
    "cogs.comic",
    # "cogs.stamp",
    # "cogs.nanka",
    store=False
)

bot.run(TOKEN)
