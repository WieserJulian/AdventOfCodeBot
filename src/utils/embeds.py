import datetime

import interactions
from interactions.ext.paginators import Paginator

today = datetime.date.today()
year = today.year

def gen_embed(bot: interactions.Client, message):
    embed = interactions.Embed("Continue: ...")
    embed.url = "https://adventofcode.com/{}/day/{}".format(year, message.split("Day ")[1][0])
    for field in message.split("<field>"):
        if field.startswith("<author>"):
            embed.set_author(bot.user.username, icon_url=bot.user.avatar.url, url=field.split("<author>")[1])
        elif field.startswith("<title>"):
            embed.title = field.split("<title>")[1]
        else:
            if len(field) <= 1024:
                embed.add_field(" ", field)
            else:
                embed.add_field("FIELD EXTENDING FAILED",
                                "**[VISIT WEBSITE TO WATCH THIS COLOSSUS](https://adventofcode.com/)**")
    return embed


def gen_leaderboard(message, database, client, discord_id, last_changed):
    fields = _generate_fields_by_json(message)
    adventname = database.get_adventname_by_discord_id(discord_id)

    score = set()
    rankes = []
    for field in fields:
        if field[0] in score:
            rankes.append(len(score))
        else:
            score.add(field[0])
            rankes.append(len(score))

    place = "" if not adventname in [field[1] for field in fields] else "Your current place is: " + str(
        rankes[[field[1] for field in fields].index(adventname)])
    embeds = []
    embed_footer = interactions.EmbedFooter(text=f'Last time refreshed: {last_changed} will updated all 30min')
    embed = interactions.Embed("Leaderboard (1-10)", description=place, footer=embed_footer)
    embed.url = "https://adventofcode.com/{}/leaderboard/private/view/{}".format(year, message['owner_id'])
    for index, field in enumerate(fields):
        mention = database.get_nickname_by_adventname(field[1])
        add = "" if mention == "" else '\t@' + mention
        rank = str(rankes[index])
        embed.add_field(str(rank) + ")\t" + field[1] + add, field[2])
        if len(embed.fields) > 9:
            embeds.append(embed)
            embed = interactions.Embed("Leaderboard ({}-{})".format(len(embeds) * 10, (len(embeds) + 1) * 10),
                                       description=place, footer=embed_footer)
    embeds.append(embed)
    return Paginator.create_from_embeds(client, *embeds)


def _generate_fields_by_json(leaderboard):
    members = leaderboard['members']
    important = []
    for member in members:
        stars = ""
        for day in members[member]['completion_day_level']:
            count = len(members[member]['completion_day_level'][day])
            stars += "⭐" if count == 2 else "✨" if count == 1 else "✹"
        stars += "✹" * (25 - len(stars))
        important.append([members[member]['local_score'], members[member]['name'], stars])
    return sorted(important, key=lambda x: -x[0])
