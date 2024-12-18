import datetime

import interactions
from interactions import EmbedFooter
from interactions.ext.paginators import Paginator

from src.utils.database import DataBase

today = datetime.date.today()
year = today.year


def gen_hint(puzzle, give_day):
    embed = interactions.Embed()
    embed.title = "Hint for Day {}".format(give_day)
    for i, puz in enumerate(puzzle):
        embed.add_field("Hint {}:".format(i + 1), "{}".format(puz))
    return embed


def gen_help():
    embed = interactions.Embed()
    embed.title = "Help"
    embed.url = "https://adventofcode.com/" + str(year)
    embed.add_field("Step 1", f"Go to [AdventOfCodeWebsite](https://adventofcode.com/{str(year)})\nRegister there under Login")
    embed.add_field("Step 2", "Under Settings in the website you find your Username\nNow Subscribe by the command:\n"
                              "/subscribe adventname: YOURUSERNAME")
    embed.add_field("Step 3", "Now ask your AdventOfCode Manager on the Server for the private Leaderboard code")
    embed.add_field("Step 4", "Have fun and a twinklie time")
    return embed


def gen_welcome(message: str):
    embed = interactions.Embed()
    embed.title = "Welcome back in the Advent Of Code "+str(year)
    embed.url = "https://adventofcode.com/" + str(year)
    embed.add_field("From AdventOfCode", message)
    embed.footer = EmbedFooter(text="Hello I am the AdventOfCode Bot\nI will help you with your AdventOfCode Journey")
    return embed


def gen_leaderboard(message, database: DataBase, client, discord_id, last_changed):
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
        stars = ["✹" for _ in range(25)]
        for day in members[member]['completion_day_level']:
            count = len(members[member]['completion_day_level'][day])
            stars[int(day)-1] = "⭐" if count == 2 else "✨" if count == 1 else "✹"
        important.append([members[member]['local_score'], members[member]['name'], "".join(stars)])
    return sorted(important, key=lambda x: -x[0])
