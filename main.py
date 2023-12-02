import datetime
import json
import logging
import os

import interactions
from interactions.ext import prefixed_commands
import requests
from dotenv import load_dotenv
from interactions.ext.prefixed_commands import prefixed_command, PrefixedHelpCommand

from src.registerd.hint import Hint
from src.registerd.message import Message
from src.utils.database import DataBase
from src.utils.embeds import gen_embed, gen_leaderboard, gen_help, gen_hint
from src.registerd.servers import Server
from src.scoreboard.scoreboard import ScoreBoard
from src.utils.text_converter import main_page_converter
from src.registerd.user import User
from src.utils.alerts import AlertHandler

bot = interactions.Client(send_command_tracebacks=False)
database = DataBase()
load_dotenv()
base_url = "https://adventofcode.com"

today = datetime.date.today()
year = today.year

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


@interactions.slash_command(name="subscribe", description="Subscribe for reminder for")
@interactions.slash_option("adventname", description="Your advent of Code Name (You find it under settings)",
                           required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("reminder", description="If you want to get reminded every day (DEFAULT=OFF)",
                           required=False, opt_type=interactions.OptionType.BOOLEAN)
async def subscribe_to_adventofcode(ctx: interactions.SlashContext, adventname: str, reminder: bool = False):
    if not database.check_user(str(ctx.author.id)):
        database.add_user(User(str(ctx.author.id), str(ctx.author.display_name), str(adventname), reminder))
        await ctx.send("Congratulations you have been subscribed", ephemeral=True)
        return
    await ctx.send("Your already registered for this Event\nIf you want to change the reminder user /reminder",
                   ephemeral=True)


@interactions.slash_command(name="unsubscribe", description="Unsubscribe from advent of code")
async def unsubscribe_to_adventofcode(ctx: interactions.SlashContext):
    database.del_user(str(ctx.author.id))
    await ctx.send("So sorry to hear that have a great time", ephemeral=True)


@interactions.slash_command(name="reminder", description="Toogle reminder")
async def toggle_reminder(ctx: interactions.SlashContext):
    value = database.toggle_reminder(str(ctx.author.id))
    await ctx.send(f"Your reminder is: {'ON' if value else 'OFF'}", ephemeral=True)


@interactions.slash_command(name="leaderboard", description="Get the private leaderboard")
async def leaderboard(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id), 0)
    if database.check_server_api(server):
        api_id = database.get_api_id_by_guild_id(str(ctx.guild.id))
        if api_id is not None:
            content, last_changed = database.get_scoreboard_and_changed(api_id)
            content_json = json.loads(content)
            paginator = gen_leaderboard(content_json, database, client=bot, discord_id=str(ctx.author.id),
                                        last_changed=last_changed)
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
    if not database.check_hints_exists(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint)):
        hint = Hint(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint), hint1, hint2)
        database.add_hints(hint)
        await ctx.send("Hint has been added for Day {}".format(day_hint), ephemeral=True)
        return
    await ctx.send("There has already been Hints for Day {} => Try update_hint".format(day_hint), ephemeral=True)


@interactions.slash_command(name="update_hint", description="Updat Hint to your server for this year")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_option("hint1", description="Hint 1", required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("hint2", description="Hint 2", required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def update_hint(ctx: interactions.SlashContext, day_hint: int, hint1: str, hint2: str):
    if database.check_hints_exists(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint)):
        hint = Hint(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint), hint1, hint2)
        database.update_hint(hint)
        await ctx.send("Hint has been updated for Day {}".format(day_hint), ephemeral=True)
        return
    await ctx.send("There were no Hints for Day {} => Try add_hint".format(day_hint), ephemeral=True)


@interactions.slash_command(name="delete_hint", description="Delete Hint from your server for this year")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def delete_hint(ctx: interactions.SlashContext, day_hint: int):
    if database.check_hints_exists(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint)):
        database.del_hint(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint))
        await ctx.send("Hint has been deleted for Day {}".format(day_hint), ephemeral=True)
        return
    await ctx.send("There were no Hints for Day {} => Try add_hint".format(day_hint), ephemeral=True)


@interactions.slash_command(name="hint", description="Get hint from server")
@interactions.slash_option("day_hint", description="The day", required=True, opt_type=interactions.OptionType.INTEGER)
async def hint(ctx: interactions.SlashContext, day_hint: int):
    if database.check_hints_exists(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint)):
        puzzles = database.get_hint(str(ctx.guild.id), "{:04d}{:02d}".format(year, day_hint))
        await ctx.send(embed=gen_hint(puzzles, day_hint), ephemeral=True)
        return
    await ctx.send("There were no Hints for Day {}".format(day_hint), ephemeral=True)


@interactions.slash_command(name="resend_message", description="Sets this channel to the publish channel")
@interactions.slash_option("day", description="The day",
                           required=True, opt_type=interactions.OptionType.INTEGER)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def resend_message(ctx: interactions.SlashContext, day: int):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    message = database.get_message("{:04d}{:02d}".format(year, day))
    if database.check_server_channel(server):
        if message is not None:
            await ctx.send(embeds=gen_embed(bot, message))
            return
        await ctx.send("No message has been found for that day", ephemeral=True)
        return
    await ctx.send("This server has not been registered a publishing channel", ephemeral=True)


@interactions.slash_command(name="publish_channel", description="Sets this channel to the publish channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def set_publish_channel(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    if not database.check_server_channel(server):
        database.add_servers(server)
        await ctx.send("This channel has been set to be a publish channel", ephemeral=True)
        return
    await ctx.send("This is already a publishing channel", ephemeral=True)


@interactions.slash_command(name="delete_leaderboard", description="Sets this channel to the publish channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def delete_leaderboard(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    if database.check_server(server):
        if database.check_server_api(server):
            api_id = database.get_api_id_by_guild_id(server.id)
            database.del_scoreboard(api_id)
            server.leader_api = None
            database.update_servers_api(server)
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
    server = Server(str(ctx.guild.id), str(ctx.channel.id), owner_id)
    if database.check_server(server):
        if not database.check_server_api(server):
            database.update_servers_api(server)
            s = requests.session()
            cookie_obj = requests.cookies.create_cookie(domain=".adventofcode.com", name="session", value=cookie)
            s.cookies.set_cookie(cookie_obj)
            content = s.get(
                base_url + r"/{}/leaderboard/private/view/{}.json".format(str(year), str(owner_id))).content.decode()
            content_json = json.loads(content)
            database.add_scoreboard(
                ScoreBoard(owner_id, datetime.datetime.now().strftime("%Y.%m.%d %H:%M"),
                           owner_id=content_json['owner_id'],
                           json_content=content, cookie_value=cookie))
            await ctx.send("Your leaderboard has been set", ephemeral=True)
            return
        await ctx.send("There is already an private leaderboard registered", ephemeral=True)
        return
    await ctx.send("This server has not been registered create an new publish channel", ephemeral=True)


@interactions.slash_command(name="remove_publish", description="Remove publishing channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def unset_publish_channel(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    if database.check_server_channel(server):
        database.del_server(Server(str(ctx.guild.id), str(ctx.channel.id)))
        await ctx.send("This is no longer a publish channel", ephemeral=True)
        return
    await ctx.send("This was not a publish channel", ephemeral=True)


@interactions.Task.create(interactions.TimeTrigger(hour=6, minute=10, utc=False))
async def reload_page():
    message, day = main_page_converter(base_url, database, year)
    if not database.check_message_exists("{:04d}{:02d}".format(year, int(day))):
        database.add_message(Message("{:04d}{:02d}".format(year, int(day)), message))


@interactions.Task.create(interactions.TimeTrigger(hour=6, minute=15, utc=False))
async def daily():
    channels = database.get_send_channels()
    message = database.get_last_message()
    users = database.get_send_users()
    for channel in channels:
        channel = bot.get_channel(channel)
        for mes in message:
            if mes.count("<embed>") == 0:
                await channel.send("@here", embeds=gen_embed(bot, mes))
            else:
                for em in mes.split("<embed>"):
                    await channel.send("@here", embeds=gen_embed(bot, em))
    for user_id in users:
        user = await bot.fetch_user(user_id)
        for mes in message:
            if mes.count("<embed>") == 0:
                await user.send(embeds=gen_embed(bot, mes))
            else:
                for em in mes.split("<embed>"):
                    await user.send(embeds=gen_embed(bot, em))


@interactions.Task.create(interactions.IntervalTrigger(minutes=20))
async def update_scoreboard():
    all_to_update = database.get_api_keys_servers()
    for api_id, server_id in all_to_update:
        owner_id, cookie_value = database.get_owner_id(api_id)
        s = requests.session()
        cookie_obj = requests.cookies.create_cookie(domain=".adventofcode.com", name="session", value=cookie_value)
        s.cookies.set_cookie(cookie_obj)
        content = s.get(
            base_url + r"/{}/leaderboard/private/view/{}.json".format(str(year), str(owner_id))).content.decode()
        content_json = json.loads(content)
        database.update_scoreboard(ScoreBoard(api_id, datetime.datetime.now().strftime("%Y.%m.%d %H:%M"),
                                              owner_id=content_json['owner_id'], json_content=content,
                                              cookie_value=None))
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
