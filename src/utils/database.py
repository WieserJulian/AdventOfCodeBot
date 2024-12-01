from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing.suite.test_reflection import users

from src.database.database_types import Base, User, Server, ScoreBoard, Hint, EventDay, AdventTable


class DataBase:

    def __init__(self, name: str = "AdventOfCode.db"):
        self.engine = create_engine(f'sqlite:///{name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_record(self, record):
        self.session.add(record)
        self.session.commit()

    def update_user(self, discord_id, **kwargs):
        user = self.session.query(User).filter_by(discord_id=discord_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.session.commit()

    def toggle_remind(self, discord_id):
        user = self.session.query(User).filter_by(discord_id=discord_id).first()
        if user:
            user.shouldremind = not user.shouldremind
            self.session.commit()
            return user.shouldremind
        return False

    def delete_user(self, discord_id):
        user = self.session.query(User).filter_by(discord_id=discord_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def update_server(self, guild_id, server: Server):
        server = self.session.query(Server).filter_by(guild_id=guild_id).first()
        if server:
            server.api_id = server.api_id
            server.channel_id = server.channel_id
            self.session.commit()

    def delete_server(self, guild_id):
        server = self.session.query(Server).filter_by(guild_id=guild_id).first()
        if server:
            self.session.delete(server)
            self.session.commit()

    def update_scoreboard(self, api_id, score_board: ScoreBoard):
        scoreboard = self.session.query(ScoreBoard).filter_by(api_id=api_id).first()
        if scoreboard:
            scoreboard.cookie_value = score_board.cookie_value
            scoreboard.owner_id = score_board.owner_id
            scoreboard.json_content = score_board.json_content
            scoreboard.last_refresh = score_board.last_refresh
            self.session.commit()

    def delete_scoreboard(self, api_id):
        scoreboard = self.session.query(ScoreBoard).filter_by(api_id=api_id).first()
        if scoreboard:
            self.session.delete(scoreboard)
            self.session.commit()

    def update_hint(self, guild_id: str, day_id: str, hintNew: Hint):
        hint = self.session.query(Hint).filter_by(guild_id=guild_id, day_id=day_id).first()
        if hint:
            hint.puzzle1 = hintNew.puzzle1
            hint.puzzle2 = hintNew.puzzle2
            self.session.commit()

    def delete_hint(self, guild_id, day_id):
        hint = self.session.query(Hint).filter_by(guild_id=guild_id, day_id=day_id).first()
        if hint:
            self.session.delete(hint)
            self.session.commit()

    def update_event_day(self, day_id: str, adventDay: EventDay):
        event_day = self.session.query(EventDay).filter_by(day_id=day_id).first()
        if event_day:
            event_day.year = adventDay.year
            event_day.link = adventDay.link
            event_day.title = adventDay.title
            event_day.description = adventDay.description
            event_day.has_been_send = adventDay.has_been_send
            self.session.commit()

    def delete_event_day(self, day_id: str):
        event_day = self.session.query(EventDay).filter_by(day_id=day_id).first()
        if event_day:
            self.session.delete(event_day)
            self.session.commit()

    def update_advent_table(self, year, adventtable: AdventTable):
        advent_table = self.session.query(AdventTable).filter_by(year=year).first()
        if advent_table:
            advent_table.title = adventtable.title
            advent_table.description = adventtable.description
            advent_table.days = adventtable.days
            self.session.commit()

    def delete_advent_table(self, year):
        advent_table = self.session.query(AdventTable).filter_by(year=year).first()
        if advent_table:
            self.session.delete(advent_table)
            self.session.commit()

    def get_user(self, discord_id: str) -> Type[User] | None:
        return self.session.query(User).filter_by(discord_id=discord_id).first()

    def get_server(self, guild_id: str) -> Type[Server] | None:
        return self.session.query(Server).filter_by(guild_id=guild_id).first()

    def get_scoreboard(self, api_id: str, owner_id: str) -> Type[ScoreBoard] | None:
        return self.session.query(ScoreBoard).filter_by(api_id=api_id, owner_id=owner_id).first()

    def get_hint(self, guild_id: str, day_id: str) -> Type[Hint] | None:
        return self.session.query(Hint).filter_by(guild_id=guild_id, day_id=day_id).first()

    def get_event_day(self, day_id: str) -> Type[EventDay] | None:
        return self.session.query(EventDay).filter_by(day_id=day_id).first()

    def get_event_day_and_ready(self, day_id: str) -> Type[EventDay] | None:
        return self.session.query(EventDay).filter_by(day_id=day_id).filter(EventDay.link.isnot(None)).first()

    def get_advent_table(self, year: str) -> Type[AdventTable] | None:
        return self.session.query(AdventTable).filter_by(year=year).first()

    def check_user(self, discord_id: str) -> bool:
        return bool(self.session.query(User).filter_by(discord_id=discord_id).first())

    def check_server(self, guild_id: str) -> bool:
        return bool(self.session.query(Server).filter_by(guild_id=guild_id).first())

    def check_server_has_api(self, guild_id: str) -> bool:
        return bool(self.session.query(Server).filter_by(guild_id=guild_id).first().api_id)

    def check_hint(self, guild_id: str, day_id: str) -> bool:
        return bool(self.session.query(Hint).filter_by(guild_id=guild_id, day_id=day_id).first())

    def check_message(self, day_id: str) -> bool:
        return bool(self.session.query(EventDay).filter_by(day_id=day_id).first())

    def check_event_day(self, day_id: str) -> bool:
        return bool(self.session.query(EventDay).filter_by(day_id=day_id).first())

    def check_advent_table(self, year: str) -> bool:
        return bool(self.session.query(AdventTable).filter_by(year=year).first())

    def get_send_channels(self) -> [str]:
        return [server.channel_id for server in self.session.query(Server).all()]

    def get_last_message(self):
        return self.session.query(EventDay).filter_by(has_been_send=False).filter(EventDay.link.isnot(None)).all()

    def get_send_users(self):
        return self.session.query(User).filter(User.shouldremind == True).all()

    def update_last_messages(self):
        self.session.query(EventDay).update({'has_been_send': True})
        self.session.commit()

    def get_all_server_with_api(self) -> [Server]:
        return self.session.query(Server).filter(Server.api_id.isnot(None)).all()

    def get_adventname_by_discord_id(self, discord_id: str) -> str:
        users = self.session.query(User).filter_by(discord_id=discord_id).first()
        if users:
            return str(users.adventname)
        return discord_id

    def get_nickname_by_adventname(self, adventname: str) -> str:
        users = self.session.query(User).filter_by(adventname=adventname).first()
        if users:
            return str(users.nickname)
        return ""
