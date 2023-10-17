import os
import datetime
import interactions
from dotenv import load_dotenv
import requests

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
@interactions.slash_option("reminder", description="If you want to get reminded every day (DEFAULT=OFF)",
                           required=False, opt_type=interactions.OptionType.BOOLEAN)
async def subscribe_to_adventofcode(ctx: interactions.SlashContext, reminder: bool = False):
    if not database.check_user(str(ctx.author.id)):
        database.add_user(User(str(ctx.author.id), str(ctx.author.display_name), reminder))
        await ctx.send("Congratulations you have been selected", ephemeral=True)
        return
    await ctx.send("Your already registered for this Event\nIf you want to change the reminder user /reminder", ephemeral=True)


@interactions.slash_command(name="unsubscribe", description="Unsubscribe from advent of code")
async def unsubscribe_to_adventofcode(ctx: interactions.SlashContext):
    database.del_user(str(ctx.author.id))
    await ctx.send("So sorry to hear that have a great time", ephemeral=True)

@interactions.slash_command(name="reminder", description="Toogle reminder")
async def toggle_reminder(ctx: interactions.SlashContext):
    value = database.toggle_reminder(str(ctx.author.id))
    await ctx.send(f"Your reminder is: {'ON' if value else 'OFF'}", ephemeral=True)

@interactions.slash_command(name="publish_channel", description="Sets this channel to the publish channel")
@interactions.slash_default_member_permission(permission=interactions.Permissions.ADMINISTRATOR)
async def set_publish_channel(ctx: interactions.SlashContext):
    server = Server(str(ctx.guild.id), str(ctx.channel.id))
    if not database.check_server(server):
        database.add_servers(server)
        await ctx.send("This channel has been set to be a publish channel", ephemeral=True)
        return
    await ctx.send("This is already a publishing channel", ephemeral=True)

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
                await channel.send("@here",embeds=gen_embed(bot, mes))
            else:
                for em in mes.split("<embed>"):
                    await channel.send("@here",embeds=gen_embed(bot, em))
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
    #TODO use the API and update it in database
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
