from src.database.database_types import AdventTable
from src.utils.types.AdventOfCodeDay import AdventOfCodeDay


class AdventOfCodeTable:
    def __init__(self, year:str, title: str, text: str, days: [AdventOfCodeDay]) -> None:
        self.year = year
        self.title = title
        self.text = text
        self.days = days

    def to_advent_table(self)->AdventTable:
        return AdventTable(year=self.year, title=self.title, description=self.text)

    def __str__(self) -> str:
        return f"AdventOfCodeTable(year={self.year}, title={self.title}, text={self.text}, days={",".join([str(day) for day in self.days])})"