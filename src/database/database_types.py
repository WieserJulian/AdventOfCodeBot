from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'USER'
    discord_id = Column(String, primary_key=True)
    nickname = Column(String)
    adventname = Column(String)
    shouldremind = Column(Boolean)

class Server(Base):
    __tablename__ = 'SERVER'
    guild_id = Column(String, primary_key=True)
    channel_id = Column(String)
    api_id = Column(String)
    owner_id = Column(String)

class ScoreBoard(Base):
    __tablename__ = 'SCOREBOARD'
    api_id = Column(String, primary_key=True)
    cookie_value = Column(String)
    owner_id = Column(String)
    json_content = Column(Text)
    last_refresh = Column(Text)

class Hint(Base):
    __tablename__ = 'HINT'
    guild_id = Column(String, primary_key=True)
    day_id = Column(String, primary_key=True)
    puzzle1 = Column(Text)
    puzzle2 = Column(Text)

class EventDay(Base):
    __tablename__ = 'EVENTDAY'
    day_id = Column(String, primary_key=True)
    year = Column(String, ForeignKey('ADVENTTABLE.year'))
    link = Column(String)
    title = Column(String)
    description = Column(String)
    has_been_send = Column(Boolean, default=False)

class AdventTable(Base):
    __tablename__ = 'ADVENTTABLE'
    year = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    days = relationship('EventDay', backref='advent_table')