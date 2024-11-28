from src.utils.AdventOfCodeDay import AdventOfCodeDay


class AdventOfCodeTable:
    def __init__(self, title: str, text: str, days: [AdventOfCodeDay]) -> None:
        self.title = title
        self.text = text
        self.days = days

    def __str__(self) -> str:
        return f"AdventOfCodeTable(title={self.title}, text={self.text}, days={",".join([str(day) for day in self.days])})"