import sqlite3

import logging

from src.message import Message
from src.servers import Server
from src.user import User


class DataBase:
    name = "AdventOfCode.db"

    def __init__(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()

    def add_user(self, user: User):
        name = "users"
        self.__create_table__(name, "id, name, reminder")
        self.cur.execute(f'INSERT INTO {name} VALUES(?,?, ?)',(user.id, user.name, user.reminder))
        self.con.commit()

    def add_message(self, message: Message):
        logging.info("[DATABASE] ", message)
        name = "messages"
        self.__create_table__(name, "id, message, sended")
        self.cur.execute(f'INSERT INTO {name} VALUES(?,?, FALSE)',(message.id, message.message))
        self.con.commit()

    def add_servers(self, server: Server):
        name = "servers"
        self.__create_table__(name, "id, channel")
        self.cur.execute(f'INSERT INTO {name} VALUES(?,?)',(server.id, server.channel))
        self.con.commit()


    def check_message_exists(self, id):
        name = "messages"
        try:
            return self.cur.execute(f'SELECT count(*) FROM {name} WHERE id=?', (id, )).fetchone()[0] != 0
        except Exception as ex:
            return False

    def check_user(self, id):
        name = "users"
        try:
            return self.cur.execute(f'SELECT count(*) FROM {name} WHERE id=?', (id,)).fetchone()[0] != 0
        except Exception as ex:
            return False

    def check_server(self, server: Server):
        name = "servers"
        try:
            return self.cur.execute(f'SELECT count(*) FROM {name} WHERE id=? AND channel=?', (server.id,server.channel)).fetchone()[0] != 0
        except Exception as ex:
            return False

    def get_last_message(self):
        name = "messages"
        res = self.cur.execute(f'SELECT message FROM {name} WHERE sended = FALSE').fetchall()
        self.cur.execute(f'Update {name} set sended = TRUE where sended = FALSE')
        self.con.commit()
        return [r[0] for r in res]

    def get_send_channels(self):
        name = "servers"
        res = self.cur.execute(f'SELECT channel FROM {name}').fetchall()
        return [r[0] for r in res]

    def get_send_users(self):
        name = "users"
        res = self.cur.execute(f'SELECT id FROM {name} WHERE reminder = TRUE').fetchall()
        return [r[0] for r in res]


    def del_user(self, id):
        name = "users"
        self.cur.execute(f'DELETE FROM {name} WHERE id=?', (id, ))
        self.con.commit()

    def del_server(self, server: Server):
        name = "servers"
        self.cur.execute(f'DELETE FROM {name} WHERE id=? AND channel=?', (server.id, server.channel))
        self.con.commit()

    def toggle_reminder(self, id):
        name = "users"
        value = self.cur.execute(f'SELECT reminder FROM {name} WHERE id = ?', (id,)).fetchone()[0]
        self.cur.execute(f'Update {name} set reminder = ? where id = ?', (not value, id))
        self.con.commit()
        return not value


    def __create_table__(self, name, columns):
        try:
            self.cur.execute(f''' SELECT count(*) FROM {name}''')
        except:
            print("error")
            self.cur.execute(f"CREATE TABLE {name}({columns})")
            self.con.commit()
