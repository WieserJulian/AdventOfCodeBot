import os

import interactions
from dotenv import load_dotenv

from src.embeds import gen_embed

bot = interactions.Client()

load_dotenv()
last_done = "17.10.2023"


@interactions.slash_command(name="subscribe", description="Subscribe for reminder for")
async def subscribe_to_adventofcode(ctx: interactions.SlashContext):
    await ctx.send("subscribe", ephemeral=True)


@interactions.slash_command(name="unsubscribe", description="Unsubscribe from advent of code")
async def unsubscribe_to_adventofcode(ctx: interactions.SlashContext):
    await ctx.send("unsubscribe", ephemeral=True)


@interactions.Task.create(interactions.TimeTrigger(hour=8, minute=52, utc=False))
async def daily():
    # TODO database request channels daily message
    channels = [1093513970729635850]
    message = ["The first puzzles will unlock on December 1st at midnight EST (UTC-5). See you then!",
               ["In the meantime, you can still access past ", "[Events]", "https://adventofcode.com/2023/events", "."],
               ["Also, starting this December, please ", "don't use AI to get on the global leaderboard",
                "https://adventofcode.com/about#ai_leaderboard", "."]]
    for channel in channels:
        channel = bot.get_channel(channel)
        await channel.send(embeds=gen_embed(bot, 0, message))


@interactions.Task.create(interactions.IntervalTrigger(minutes=30))
async def update_scoreboard():
    #TODO use the API and update it in database
    pass


@interactions.listen()
async def on_startup():
    print("=" * 50 + "\nBot Startet\n" + "=" * 50)
    print("Starting Tasks")
    daily.start()
    update_scoreboard.start()
    print("Started Tasks\n" + "=" * 50)


bot.start(os.getenv("BOT_TOKEN"))
