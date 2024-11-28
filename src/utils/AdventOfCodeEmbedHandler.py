from src.utils.AdventOfCodeTable import AdventOfCodeTable


class AdventOfCodeEmbedHandler:

    def __init__(self, table: AdventOfCodeTable) -> None:
        self.table = table
        self.embeds = {}
        self.__split_up_days()
        pass

    def __split_up_days(self):
        for day in self.table.days:
            days_embed = []
            text = day.text
            words = text.split()
            current_embed = ""

            for word in words:
                if len(current_embed) + len(word) + 1 > 4096:
                    days_embed.append(current_embed)
                    current_embed = word
                else:
                    if current_embed:
                        current_embed += " " + word
                    else:
                        current_embed = word

            if current_embed:
                days_embed.append(current_embed)

            self.embeds[day.day] = days_embed
