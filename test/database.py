import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.database_types import Base, User, Server, ScoreBoard, Hint, EventDay, AdventTable
from src.utils.database import DataBase

class TestDataBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.db = DataBase(":memory:")
        cls.db.session = cls.session

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.engine.dispose()

    def setUp(self):
        self.session.begin_nested()

    def tearDown(self):
        self.session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_user_creation(self):
        user = User(discord_id="1", nickname="TestUser", adventname="TestUser", shouldremind=True)
        self.db.add_record(user)
        self.assertIsNotNone(self.db.get_user("1"))

    def test_user_update(self):
        user = User(discord_id="1", nickname="TestUser", adventname="TestUser", shouldremind=True)
        self.db.add_record(user)
        self.db.update_user("1", nickname="UpdatedUser")
        updated_user = self.db.get_user("1")
        self.assertEqual(updated_user.nickname, "UpdatedUser")

    def test_user_deletion(self):
        user = User(discord_id="1", nickname="TestUser", adventname="TestUser", shouldremind=True)
        self.db.add_record(user)
        self.db.delete_user("1")
        self.assertIsNone(self.db.get_user("1"))

    def test_hint_creation(self):
        hint = Hint(guild_id="1", day_id="2", puzzle1="T1", puzzle2="T2")
        self.db.add_record(hint)
        self.assertIsNotNone(self.db.get_hint("1", "2"))

    def test_hint_update(self):
        hint = Hint(guild_id="1", day_id="2", puzzle1="T1", puzzle2="T2")
        self.db.add_record(hint)
        updated_hint = Hint(guild_id="1", day_id="2", puzzle1="T3", puzzle2="T4")
        self.db.update_hint("1", "2", updated_hint)
        self.assertEqual(self.db.get_hint("1", "2").puzzle1, "T3")
        self.assertEqual(self.db.get_hint("1", "2").puzzle2, "T4")

    def test_hint_deletion(self):
        hint = Hint(guild_id="1", day_id="2", puzzle1="T1", puzzle2="T2")
        self.db.add_record(hint)
        self.db.delete_hint("1", "2")
        self.assertIsNone(self.db.get_hint("1", "2"))

    def test_server_creation(self):
        server = Server(guild_id="1", channel_id="2", api_id="3", owner_id="4")
        self.db.add_record(server)
        self.assertIsNotNone(self.db.get_server("1"))

    def test_server_update(self):
        server = Server(guild_id="1", channel_id="2", api_id="3", owner_id="4")
        self.db.add_record(server)
        self.db.update_server("1", channel_id="5")
        updated_server = self.db.get_server("1")
        self.assertEqual(updated_server.channel_id, "5")

    def test_server_deletion(self):
        server = Server(guild_id="1", channel_id="2", api_id="3", owner_id="4")
        self.db.add_record(server)
        self.db.delete_server("1")
        self.assertIsNone(self.db.get_server("1"))

    def test_scoreboard_creation(self):
        scoreboard = ScoreBoard(api_id="1", cookie_value="2", owner_id="3", json_content="4", last_refresh="5")
        self.db.add_record(scoreboard)
        self.assertIsNotNone(self.db.get_scoreboard("1"))

    def test_scoreboard_update(self):
        scoreboard = ScoreBoard(api_id="1", cookie_value="2", owner_id="3", json_content="4", last_refresh="5")
        self.db.add_record(scoreboard)
        updated_scoreboard = ScoreBoard(api_id="1", cookie_value="6", owner_id="7", json_content="8", last_refresh="9")
        self.db.update_scoreboard("1", updated_scoreboard)
        self.assertEqual(self.db.get_scoreboard("1").cookie_value, "6")
        self.assertEqual(self.db.get_scoreboard("1").owner_id, "7")
        self.assertEqual(self.db.get_scoreboard("1").json_content, "8")
        self.assertEqual(self.db.get_scoreboard("1").last_refresh, "9")

    def test_scoreboard_deletion(self):
        scoreboard = ScoreBoard(api_id="1", cookie_value="2", owner_id="3", json_content="4", last_refresh="5")
        self.db.add_record(scoreboard)
        self.db.delete_scoreboard("1")
        self.assertIsNone(self.db.get_scoreboard("1"))

    def test_eventday_creation(self):
        eventday = EventDay(day_id="1", year="2", link="3", title="4", description="5", has_been_send=True)
        self.db.add_record(eventday)
        self.assertIsNotNone(self.db.get_event_day("1"))

    def test_eventday_update(self):
        eventday = EventDay(day_id="1", year="2", link="3", title="4", description="5", has_been_send=True)
        self.db.add_record(eventday)
        updated_eventday = EventDay(day_id="1", year="2", link="6", title="7", description="8", has_been_send=False)
        self.db.update_event_day("1", updated_eventday)
        self.assertEqual(self.db.get_event_day("1").link, "6")
        self.assertEqual(self.db.get_event_day("1").title, "7")
        self.assertEqual(self.db.get_event_day("1").description, "8")
        self.assertEqual(self.db.get_event_day("1").has_been_send, False)

    def test_eventday_deletion(self):
        eventday = EventDay(day_id="1", year="2", link="3", title="4", description="5", has_been_send=True)
        self.db.add_record(eventday)
        self.db.delete_event_day("1")
        self.assertIsNone(self.db.get_event_day("1"))

    def test_adventtable_creation(self):
        adventtable = AdventTable(year="1", title="2", description="3")
        self.db.add_record(adventtable)
        self.assertIsNotNone(self.db.get_advent_table("1"))

    def test_adventtable_update(self):
        adventtable = AdventTable(year="1", title="2", description="3")
        self.db.add_record(adventtable)
        updated_adventtable = AdventTable(year="1", title="4", description="5")
        self.db.update_advent_table("1", updated_adventtable)
        self.assertEqual(self.db.get_advent_table("1").title, "4")
        self.assertEqual(self.db.get_advent_table("1").description, "5")

    def test_adventtable_deletion(self):
        adventtable = AdventTable(year="1", title="2", description="3")
        self.db.add_record(adventtable)
        self.db.delete_advent_table("1")
        self.assertIsNone(self.db.get_advent_table("1"))

if __name__ == '__main__':
    unittest.main()