import interactions


def gen_embed(bot, day, message):
    embed = interactions.Embed("Advent Of Code Day:{}".format(day))
    for mes in message:
        if type(mes) is list:
            embed.add_field(" ", "{}[{}]({}){}".format(mes[0], mes[1], mes[2], mes[3]))
        else:
            embed.add_field(" ", mes)
    return embed