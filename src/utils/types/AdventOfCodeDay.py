from src.database.database_types import EventDay


class AdventOfCodeDay:
    def __init__(self, day_id: str,year:str, link: str, title: str, description: [str]) -> None:
        self.day_id = day_id
        self.year = year
        self.link = link
        self.title = title
        self.description = description

    def to_event_day(self)->EventDay:
        return EventDay(day_id=self.day_id,year=self.year,link=self.link, title=self.title, description=self.description)

    @staticmethod
    def from_event_day(event_day:EventDay):
        return AdventOfCodeDay(day_id=event_day.day_id, year=event_day.year, link=event_day.link, title=event_day.title, description=event_day.description)

    def __str__(self) -> str:
        return f"AdventOfCodeDay(day={self.day_id}, link={self.link})"