import datetime
import os

import interactions
import requests
from dotenv import load_dotenv

from src.database import DataBase
from src.embeds import gen_embed
from src.servers import Server
from src.text_converter import main_page_converter
from src.user import User

bot = interactions.Client()
database = DataBase()
load_dotenv()
base_url = "https://adventofcode.com"

today = datetime.date.today()
year = today.year


@interactions.slash_command(name="subscribe", description="Subscribe for reminder for")
@interactions.slash_option("adventname", description="Your advent of Code Name (You find it under settings)",
                           required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_option("reminder", description="If you want to get reminded every day (DEFAULT=OFF)",
                           required=False, opt_type=interactions.OptionType.BOOLEAN)
async def subscribe_to_adventofcode(ctx: interactions.SlashContext, adventname: str, reminder: bool = False):
    if not database.check_user(str(ctx.author.id)):
        database.add_user(User(str(ctx.author.id), str(ctx.author.display_name), str(adventname), reminder))
        await ctx.send("Congratulations you have been selected", ephemeral=True)
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
async def toggle_reminder(ctx: interactions.SlashContext):
    await ctx.send(f"WORK IN PROGRESS", ephemeral=True)


@interactions.slash_command(name="publish_channel", description="Sets this channel to the publish channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def set_publish_channel(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    if not database.check_server(server):
        database.add_servers(server)
        await ctx.send("This channel has been set to be a publish channel", ephemeral=True)
        return
    await ctx.send("This is already a publishing channel", ephemeral=True)
@interactions.slash_command(name="set_leaderboard", description="Sets this channel to the publish channel")
@interactions.slash_option("id", description="The api key",
                           required=True, opt_type=interactions.OptionType.STRING)
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def set_leaderboard(ctx: interactions.SlashContext, id: str):
    server = Server(str(ctx.guild.id), str(ctx.channel.id), id)
    if database.check_server(server):
        if not database.check_server_api(server):
            database.update_servers_api(server)
            await ctx.send("Your leaderboard has been set", ephemeral=True)
            return
        await ctx.send("There is already an private leaderboard registered", ephemeral=True)
        return
    await ctx.send("This channel has not been registered a publishing channel", ephemeral=True)

@interactions.slash_command(name="remove_publish", description="Remove publishing channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def unset_publish_channel(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    if database.check_server(server):
        database.del_server(Server(str(ctx.guild.id), str(ctx.channel.id)))
        await ctx.send("This is no longer a publish channel", ephemeral=True)
        return
    await ctx.send("This was not a publish channel", ephemeral=True)


@interactions.Task.create(interactions.TimeTrigger(hour=5, minute=0, utc=False))
async def reload_page():
    main_page_converter(base_url, database, year)


@interactions.Task.create(interactions.TimeTrigger(hour=6, minute=0, utc=False))
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


@interactions.Task.create(interactions.IntervalTrigger(minutes=30))
async def update_scoreboard():
    all_to_update = database.get_api_keys_servers()
    for api_key in api_keys:
        content = requests.get(base_url + r"/{}/leaderboard/private/view/{}.json".format(str(year), str(api_key)))
        await
    pass


@interactions.listen()
async def on_startup():
    print("=" * 50 + "\nBot Startet\n" + "=" * 50)
    print("Starting Tasks")
    reload_page.start()
    daily.start()
    update_scoreboard.start()
    print("Started Tasks\n" + "=" * 50)


bot.start(os.getenv("BOT_TOKEN"))
