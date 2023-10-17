import interactions


def gen_embed(bot: interactions.Client, message):
    embed = interactions.Embed("Continue: ...")
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
