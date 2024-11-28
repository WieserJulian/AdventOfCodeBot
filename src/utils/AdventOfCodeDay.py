class AdventOfCodeDay:
    def __init__(self, day: int, link: str, title: str, text: [str]) -> None:
        self.day = day
        self.link = link
        self.title = title
        self.text = text

    def __str__(self) -> str:
        return f"AdventOfCodeDay(day={self.day}, link={self.link})"