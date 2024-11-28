import datetime

import interactions

from src.utils.types.AdventOfCodeDay import AdventOfCodeDay

MAX_LENGTH_FIELD = 1024
MAX_LENGTH_EMBED = 6000


class AdventOfCodeEmbedHandler:
    today = datetime.date.today()
    year = "{:04d}".format(today.year)

    def __init__(self, day: AdventOfCodeDay) -> None:
        self.day = day
        self.split = []
        self.multiple_messages = False
        self.__split_up_message()

    def get_embeds(self, bot: interactions.Client):
        embeds = []
        if self.multiple_messages:
            for i, day in enumerate(self.split):
                embeds.append(self.__gen_embed(bot, day, i == 0))
        else:
            embeds.append(self.__gen_embed(bot, self.split, True))
        return embeds

    def __gen_embed(self, bot: interactions.Client, messages: [str], isFirst: bool = False):
        embed = interactions.Embed("Continue: ...")
        embed.url = "https://adventofcode.com/{}/day/{}".format(self.year, int(self.day.day_id[4:]))
        embed.set_author(bot.user.username, icon_url=bot.user.avatar.url,
                         url="https://adventofcode.com/" + str(self.year))
        if isFirst:
            embed.title = self.day.title
        for message in messages:
            embed.add_field(" ", message, inline=False)
        return embed

    def __split_up_exceeding_message(self):
        max_length = MAX_LENGTH_EMBED
        description = self.day.description
        return [description[i:i + max_length] for i in range(0, len(description), max_length)]

    def __split_up_message(self):
        if len(self.day.description) < 6000:
            messages = [self.day.description]
        else:
            messages = self.__split_up_exceeding_message()
            self.multiple_messages = True

        embed = []
        for message in messages:
            field = []
            text = message
            words = text.split()
            current_embed = ""

            for word in words:
                if len(current_embed) + len(word) + 1 > MAX_LENGTH_FIELD:
                    field.append(current_embed)
                    current_embed = word
                else:
                    if current_embed:
                        current_embed += " " + word
                    else:
                        current_embed = word

            if current_embed:
                field.append(current_embed)
            embed.append(field)

        if not self.multiple_messages:
            self.split = embed[0]
        else:
            self.split = embed
