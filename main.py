import datetime
import json
import logging
import os

import interactions
import requests
from dotenv import load_dotenv

from src.database.database_types import User, Server, Hint, ScoreBoard
from src.utils.alerts import AlertHandler
from src.utils.database import DataBase
from src.utils.embeds import gen_leaderboard, gen_help, gen_hint, gen_welcome
from src.utils.text_converter import convert_url_to_day_object
from src.utils.types.AdventOfCodeDay import AdventOfCodeDay
from src.utils.types.AdventOfCodeEmbedHandler import AdventOfCodeEmbedHandler
from src.utils.util import day_id

bot = interactions.Client(send_command_tracebacks=False)
database = DataBase()
load_dotenv()
base_url = "https://adventofcode.com"

today = datetime.date.today()
year = "{:04d}".format(today.year)

level = logging.WARN
logging.basicConfig(filename='adventofcode.log', encoding='utf-8')
logging.getLogger("requests").disabled = True
logger = logging.getLogger()
logger.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

alertHandler = AlertHandler(url=os.getenv("NTFY-URL"))
alertHandler.setLevel(level)
alertHandler.setFormatter(formatter)
logger.addHandler(alertHandler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


@interactions.slash_command(name="subscribe", description="Subscribe for reminder for")
@interactions.slash_option("adventname", description="Your advent of Code Name (You find it under settings)",
                           required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("reminder", description="If you want to get reminded every day (DEFAULT=OFF)",
                           required=False, opt_type=interactions.OptionType.BOOLEAN)
async def subscribe_to_adventofcode(ctx: interactions.SlashContext, adventname: str, reminder: bool = False):
    if not database.check_user(str(ctx.author.id)):
        database.add_record(
            User(discord_id=str(ctx.author.id), nickname=str(ctx.author.display_name), adventname=adventname,
                 shouldremind=reminder))
        await ctx.send("Congratulations you have been subscribed", ephemeral=True)
        return
    await ctx.send("Your already registered for this Event\nIf you want to change the reminder user /reminder",
                   ephemeral=True)


@interactions.slash_command(name="unsubscribe", description="Unsubscribe from advent of code")
async def unsubscribe_to_adventofcode(ctx: interactions.SlashContext):
    database.delete_user(str(ctx.author.id))
    await ctx.send("So sorry to hear that have a great time", ephemeral=True)


@interactions.slash_command(name="reminder", description="Toogle reminder")
async def toggle_reminder(ctx: interactions.SlashContext):
    value = database.toggle_remind(str(ctx.author.id))
    await ctx.send(f"Your reminder is: {'ON' if value else 'OFF'}", ephemeral=True)


@interactions.slash_command(name="leaderboard", description="Get the private leaderboard")
async def leaderboard(ctx: interactions.SlashContext):
    if database.check_server_has_api(str(ctx.guild.id)):
        server = database.get_server(str(ctx.guild.id))
        scoreBoard = database.get_scoreboard(server.api_id, server.owner_id)
        content_json = json.loads(scoreBoard.json_content.replace("'","\""))
        paginator = gen_leaderboard(content_json, database, client=bot, discord_id=str(ctx.author.id),
                                    last_changed=scoreBoard.last_refresh)
        await paginator.send(ctx)
        return

    await ctx.send("There was no leaderboard. You might want to ask your admin to create one", ephemeral=True)


@interactions.slash_command(name="help", description="Shows you how to start")
async def help_(ctx: interactions.SlashContext):
    await ctx.send(embeds=gen_help(), ephemeral=True)


@interactions.slash_command(name="show_help_permanently", description="Shows you how to start")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def show_help_permanently(ctx: interactions.SlashContext):
    await ctx.send(embeds=gen_help())


@interactions.slash_command(name="add_hint", description="Add Hint to your server for this year")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_option("hint1", description="Hint 1", required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("hint2", description="Hint 2", required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def add_hint(ctx: interactions.SlashContext, day_hint: int, hint1: str, hint2: str):
    if not database.check_hint(str(ctx.guild.id), day_id(year, day_hint)):
        hint = Hint(guild_id=str(ctx.guild.id), day_id=day_id(year, day_hint), puzzle1=hint1,
                    puzzle2=hint2)
        database.add_record(hint)
        await ctx.send("Hint has been added for Day {}".format(day_hint), ephemeral=True)
        return
    await ctx.send("There has already been Hints for Day {} => Try update_hint".format(day_hint), ephemeral=True)


@interactions.slash_command(name="update_hint", description="Updat Hint to your server for this year")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_option("hint1", description="Hint 1", required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("hint2", description="Hint 2", required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def update_hint(ctx: interactions.SlashContext, day_hint: int, hint1: str, hint2: str):
    if database.check_hint(str(ctx.guild.id), day_id(year, day_hint)):
        hint = Hint(guild_id=str(ctx.guild.id), day_id=day_id(year, day_hint), puzzle1=hint1,
                    puzzle2=hint2)
        database.update_hint(hint)
        await ctx.send("Hint has been updated for Day {}".format(day_hint), ephemeral=True)
        return
    await ctx.send("There were no Hints for Day {} => Try add_hint".format(day_hint), ephemeral=True)


@interactions.slash_command(name="delete_hint", description="Delete Hint from your server for this year")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def delete_hint(ctx: interactions.SlashContext, day_hint: int):
    if database.check_hint(str(ctx.guild.id), day_id(year, day_hint)):
        database.delete_hint(str(ctx.guild.id), day_id(year, day_hint))
        await ctx.send("Hint has been deleted for Day {}".format(day_hint), ephemeral=True)
        return
    await ctx.send("There were no Hints for Day {} => Try add_hint".format(day_hint), ephemeral=True)


@interactions.slash_command(name="hint", description="Get hint from server")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
async def hint(ctx: interactions.SlashContext, day_hint: int):
    if database.check_hint(str(ctx.guild.id), day_id(year, day_hint)):
        puzzles = database.get_hint(str(ctx.guild.id), day_id(year, day_hint))
        await ctx.send(embed=gen_hint(puzzles, day_hint), ephemeral=True)
        return
    await ctx.send("There were no Hints for Day {}".format(day_hint), ephemeral=True)


@interactions.slash_command(name="resend_message", description="Sets this channel to the publish channel")
@interactions.slash_option("day", description="The day",
                           required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def resend_message(ctx: interactions.SlashContext, day: int):
    server = database.get_server(str(ctx.guild.id))
    if day == 0:
        table = database.get_advent_table(year)
        if server is not None:
            if table is not None:
                embed = gen_welcome(table.description)
                await ctx.send(embed=embed)
                return
            await ctx.send("No message has been found for that day", ephemeral=True)
            return
        await ctx.send("This server has not been registered a publishing channel", ephemeral=True)
        return
    message = database.get_event_day_and_ready(day_id(year, day))
    if server is not None:
        if message is not None:
            message = AdventOfCodeDay.from_event_day(message)
            embedhandler = AdventOfCodeEmbedHandler(message)
            embeds = embedhandler.get_embeds(bot)
            if embedhandler.multiple_messages:
                for embed in embeds:
                    await ctx.send(embeds=embed)
                return
            await ctx.send(embeds=embeds)
            return
        await ctx.send("No message has been found for that day", ephemeral=True)
        return
    await ctx.send("This server has not been registered a publishing channel", ephemeral=True)


@interactions.slash_command(name="publish_channel", description="Sets this channel to the publish channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def set_publish_channel(ctx: interactions.SlashContext):
    if not database.check_server(str(ctx.guild.id)):
        server = Server(guild_id=str(ctx.guild.id), channel_id=str(ctx.channel.id))
        database.add_record(server)
        await ctx.send("This channel has been set to be a publish channel", ephemeral=True)
        return
    await ctx.send("This is already a publishing channel", ephemeral=True)


@interactions.slash_command(name="delete_leaderboard", description="Sets this channel to the publish channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def delete_leaderboard(ctx: interactions.SlashContext):
    guild_id = str(ctx.guild.id)
    if database.check_server(guild_id):
        if database.check_server_has_api(guild_id):
            server = database.get_server(guild_id=guild_id)
            database.delete_scoreboard(server.api_id)
            server.api_id = None
            database.update_server(server)
            await ctx.send("Your leaderboard has been deleted", ephemeral=True)
            return
        await ctx.send("There was no leaderboard. You might want to create one? (/set_leaderboard)", ephemeral=True)
        return
    await ctx.send("This server has not been registered", ephemeral=True)


@interactions.slash_command(name="set_leaderboard", description="Sets this channel to the publish channel")
@interactions.slash_option("owner_id", description="The number after /view/<number>",
                           required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("cookie", description="Cookie value from Session store",
                           required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def set_leaderboard(ctx: interactions.SlashContext, owner_id: str, cookie: str):
    guild_id = str(ctx.guild.id)
    if database.check_server(guild_id):
        if not database.check_server_has_api(guild_id):
            server = database.get_server(guild_id=guild_id)
            server.owner_id = owner_id
            server.api_id = cookie
            database.update_server(guild_id, server)
            s = requests.session()
            cookie_obj = requests.cookies.create_cookie(domain=".adventofcode.com", name="session", value=cookie)
            s.cookies.set_cookie(cookie_obj)
            content = s.get(
                base_url + r"/{}/leaderboard/private/view/{}.json".format(str(year), str(owner_id))).content.decode()
            content_json = str(json.loads(content))
            scoreboard = ScoreBoard(api_id=server.api_id, owner_id=owner_id, cookie_value=cookie, json_content=content_json,
                                    last_refresh=datetime.datetime.now().strftime("%Y.%m.%d %H:%M"))
            database.add_record(scoreboard)
            await ctx.send("Your leaderboard has been set", ephemeral=True)
            return
        await ctx.send("There is already an private leaderboard registered", ephemeral=True)
        return
    await ctx.send("This server has not been registered create an new publish channel", ephemeral=True)


@interactions.slash_command(name="remove_publish", description="Remove publishing channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def unset_publish_channel(ctx: interactions.SlashContext):
    server = database.get_server(str(ctx.guild.id))
    if server.channel_id == str(ctx.channel.id):
        database.delete_server(str(ctx.guild.id))
        await ctx.send("This is no longer a publish channel", ephemeral=True)
        return
    await ctx.send("This was not a publish channel", ephemeral=True)


@interactions.Task.create(interactions.TimeTrigger(hour=6, minute=10, utc=False))
async def reload_page():
    table = convert_url_to_day_object(base_url, year)
    if table is None:
        return
    if not database.check_advent_table(year):
        database.add_record(table.to_advent_table())
    for day in table.days:
        if not database.check_event_day(day.day_id):
            database.add_record(day.to_event_day())


@interactions.Task.create(interactions.TimeTrigger(hour=6, minute=15, utc=False))
async def daily():
    channels = database.get_send_channels()
    messages = database.get_last_message()
    users = database.get_send_users()
    for channel in channels:
        channel = bot.get_channel(channel)
        for message in messages:
            message = AdventOfCodeDay.from_event_day(message)
            embedhandler = AdventOfCodeEmbedHandler(message)
            embeds = embedhandler.get_embeds(bot)
            if embedhandler.multiple_messages:
                for i, embed in enumerate(embeds):
                    await channel.send("@here" if i == 0 else "", embeds=embed)
                return
            await channel.send("@here", embeds=embeds)
    for loadedUser in users:
        user = await bot.fetch_user(str(loadedUser.discord_id))
        for message in messages:
            message = AdventOfCodeDay.from_event_day(message)
            embedhandler = AdventOfCodeEmbedHandler(message)
            embeds = embedhandler.get_embeds(bot)
            if embedhandler.multiple_messages:
                for i, embed in enumerate(embeds):
                    await user.send("@here" if i == 0 else "", embeds=embed)
                return
            await user.send("@here", embeds=embeds)
    database.update_last_messages()


@interactions.Task.create(interactions.IntervalTrigger(minutes=20))
async def update_scoreboard():
    servers = database.get_all_server_with_api()
    for server in servers:
        scoreboard = database.get_scoreboard(server.api_id, server.owner_id)
        s = requests.session()
        cookie_obj = requests.cookies.create_cookie(domain=".adventofcode.com", name="session",
                                                    value=scoreboard.cookie_value)
        s.cookies.set_cookie(cookie_obj)
        content = s.get(
            base_url + r"/{}/leaderboard/private/view/{}.json".format(str(year), str(server.owner_id))).content.decode()
        content_json = str(json.loads(content))
        scoreboard = ScoreBoard(api_id=server.api_id, owner_id=server.owner_id,  cookie_value=scoreboard.cookie_value, json_content=content_json,
                                last_refresh=datetime.datetime.now().strftime("%Y.%m.%d %H:%M"))
        database.update_scoreboard(server.api_id, scoreboard)
    pass


@interactions.listen()
async def on_error(error: interactions.api.events.Error):
    print(f"```\n{error.source}\n{error.error}\n```")
    logging.error(f"```\n{error.source}\n{error.error}\n```")


@interactions.listen()
async def on_startup():
    print("=" * 50 + "\nBot Startet\n" + "=" * 50)
    print("Starting Tasks")
    reload_page.start()
    daily.start()
    update_scoreboard.start()
    await reload_page()
    await daily()
    await update_scoreboard()
    print("Started Tasks\n" + "=" * 50)


def main():
    try:
        bot.start(os.getenv("BOT_TOKEN"))
    except Exception as ex:
        logger.critical("Restart Bot", ex)
        main()


if __name__ == '__main__':
    main()
