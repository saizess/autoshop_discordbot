import disnake
from disnake.ext import commands
from config import TOKEN
import os
from database import editdb


bot = commands.Bot()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print("Bot started!")

#bot starter
editdb.create_db()
editdb.createtables()
bot.run(TOKEN)