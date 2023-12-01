import sqlite3

from src.registerd.message import Message
from src.registerd.servers import Server
from src.registerd.user import User
from src.scoreboard.scoreboard import ScoreBoard


class DataBase:
    name = "AdventOfCode.db"

    def __init__(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()
        self.__init_database__()

    def __init_database__(self):
        database_layout = {
            'USER': "discord_id, nickname, adventname, shouldremind",
            'MESSAGE': "day_id, message, isSent",
            'SERVER': "guild_id, channel_id, api_id",
            'SCOREBOARD': "api_id, cookie_value, owner_id, json_content, last_refresh"
        }
        for layout in database_layout:
            self.__create_table__(layout, database_layout[layout])

    def add_user(self, user: User):
        self.cur.execute(f'INSERT INTO USER VALUES(?,?, ?, ?)',
                         (user.id, user.name, user.advent_of_code_name, user.reminder))
        self.con.commit()

    def add_message(self, message: Message):
        self.cur.execute(f'INSERT INTO MESSAGE VALUES(?,?, FALSE)', (message.id, message.message))
        self.con.commit()

    def add_servers(self, server: Server):
        self.cur.execute(f'INSERT INTO SERVER VALUES(?,?,?)', (server.id, server.channel, server.leader_api))
        self.con.commit()

    def add_scoreboard(self, scoreboard: ScoreBoard):
        self.cur.execute(f'INSERT INTO SCOREBOARD VALUES(?,?,?, ?, ?)',
                         (scoreboard.id, scoreboard.cookie_value, scoreboard.owner_id,
                          scoreboard.json_content, scoreboard.last_refresh))
        self.con.commit()

    def check_message_exists(self, id):
        try:
            res = self.cur.execute(f'SELECT count(*) FROM MESSAGE WHERE day_id=?', (id,)).fetchone()
            if res is None:
                return False
            if res[0] is None:
                return False
            return res[0] != 0
        except Exception as ex:
            return False

    def check_user(self, id):
        try:
            res = self.cur.execute(f'SELECT count(*) FROM USER WHERE discord_id=?', (id,)).fetchone()
            if res is None:
                return False
            if res[0] is None:
                return False
            return res[0] != 0
        except Exception as ex:
            return False

    def check_server_channel(self, server: Server):
        try:
            res = self.cur.execute(f'SELECT count(*) FROM SERVER WHERE guild_id=? AND channel_id=?',
                                    (server.id, server.channel)).fetchone()
            if res is None:
                return False
            if res[0] is None:
                return False
            return res[0] != 0
        except Exception as ex:
            return False

    def check_server(self, server: Server):
        try:
            return self.cur.execute(f'SELECT count(*) FROM SERVER WHERE guild_id=? ',
                                    (server.id, )).fetchone()[0] != 0
        except Exception as ex:
            return False

    def check_server_api(self, server: Server):
        try:
            res = self.cur.execute(f'SELECT api_id FROM SERVER WHERE guild_id=?',(server.id, )).fetchone()
            if res is None:
                return False
            if res[0] is None or res[0] == "":
                return False
            return True
        except Exception as ex:
            return False

    def get_last_message(self):
        res = self.cur.execute(f'SELECT message FROM MESSAGE WHERE isSent = FALSE').fetchall()
        self.cur.execute(f'Update MESSAGE set isSent = TRUE where isSent = FALSE')
        self.con.commit()
        return [r[0] for r in res]

    def get_message(self, id):
        res = self.cur.execute(f'SELECT message FROM MESSAGE WHERE day_id = ?', (id, )).fetchone()
        if res is not None:
            return res[0]
        else:
            return None

    def get_api_keys_servers(self):
        res = self.cur.execute('SELECT api_id, guild_id FROM SERVER WHERE api_id is not null').fetchall()
        return [list(r) for r in res]

    def get_api_id_by_guild_id(self, id):
        res = self.cur.execute('SELECT api_id FROM SERVER WHERE guild_id = ?', (str(id),)).fetchone()
        return res[0]

    def get_owner_id(self, id):
        res = self.cur.execute('SELECT owner_id, cookie_value FROM SCOREBOARD WHERE api_id = ?', (str(id),)).fetchone()
        return tuple(res)

    def get_send_channels(self):
        res = self.cur.execute(f'SELECT channel_id FROM SERVER').fetchall()
        return [r[0] for r in res]

    def get_scoreboard_and_changed(self, id):
        res = self.cur.execute(f'SELECT json_content,last_refresh FROM SCOREBOARD WHERE api_id = ?', (id,)).fetchone()
        return tuple(res)

    def get_nickname_by_adventname(self, name):
        res = self.cur.execute(f'SELECT nickname FROM USER WHERE adventname = ?', (name,)).fetchone()
        return res[0] if res is not None else ""

    def get_adventname_by_discord_id(self, discord_id):
        res = self.cur.execute(f'SELECT adventname FROM USER WHERE discord_id = ?', (discord_id,)).fetchone()
        return res[0] if res is not None else ""

    def get_send_users(self):
        res = self.cur.execute(f'SELECT discord_id FROM USER WHERE shouldremind = TRUE').fetchall()
        return [r[0] for r in res]

    def del_user(self, id):
        self.cur.execute(f'DELETE FROM USER WHERE discord_id=?', (id,))
        self.con.commit()

    def del_server(self, server: Server):
        self.cur.execute(f'DELETE FROM SERVER WHERE guild_id=? AND channel_id=?', (server.id, server.channel))
        self.con.commit()

    def del_scoreboard(self, api_id):
        self.cur.execute('DELETE FROM SCOREBOARD WHERE api_id=? ', (api_id,))
        self.con.commit()

    def toggle_reminder(self, id):
        value = self.cur.execute(f'SELECT shouldremind FROM USER WHERE discord_id = ?', (id,)).fetchone()[0]
        self.cur.execute(f'Update USER set shouldremind = ? where discord_id = ?', (not value, id))
        self.con.commit()
        return not value

    def update_servers_api(self, server):
        self.cur.execute(f'Update SERVER set api_id = ? where guild_id = ?', (server.leader_api, server.id))
        self.con.commit()

    def update_scoreboard(self, scoreboard: ScoreBoard):
        self.cur.execute(f'Update SCOREBOARD set json_content = ?, last_refresh=? WHERE api_id = ?',
                         (scoreboard.json_content,scoreboard.last_refresh, scoreboard.id))
        self.con.commit()

    def __create_table__(self, name, columns):
        try:
            self.cur.execute(f"CREATE TABLE {name}({columns})")
            self.con.commit()
        except Exception as ex:
            print(ex)
