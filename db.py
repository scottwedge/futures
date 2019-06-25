import sqlite3
from pypika import Query

dbLocation = "./futures.db"

values_table = "SP_500_values"
values_columns = ["resistance_1", "resistance_2", "pivot", "support_1", "support_2"]
trades_table = "positions"
trades_columns = ["type", "price", "test"]


sql_create_values_table = """CREATE TABLE IF NOT EXISTS SP_500_values (
                                        date REAL PRIMARY KEY NOT NULL DEFAULT (julianday('now')),
                                        resistance_1 REAL,
                                        resistance_2 REAL,
                                        pivot REAL,
                                        support_1 REAL,
                                        support_2 REAL 
                                    );"""

sql_create_trades_table = """CREATE TABLE IF NOT EXISTS positions (
                                        date REAL PRIMARY KEY NOT NULL DEFAULT (julianday('now')),
                                        type INTEGER,
                                        price REAL,
                                        test INTEGER
                                    );"""

select_values = """SELECT datetime(date, 'unixepoch', 'localtime') as date, resistance_1, resistance_2, pivot, support_1, support_2 FROM SP_500_values;"""
clear_values = """DELETE FROM SP_500_values;"""

sql_insert_trade = """INSERT INTO positions (type, price, test) VALUES (?, ?, ?);"""

select_trades = """SELECT datetime(date, 'unixepoch', 'localtime') as date, type, price, test FROM positions;"""
clear_trades = """DELETE FROM positions;"""


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(dbLocation, isolation_level=None)

    def close(self):
        """ close a connection to a SQLite database """
        try:
            self.conn.close()
            print("Connection closed")
        except Exception as e:
            print(e)

    def execute_statement(self, sql):
        if self.conn is not None:
            try:
                self.conn.cursor().execute(sql)
            except Exception as e:
                print("exception executing: " + str(e))
        else:
            print("No connection to db")

    def store_trade(self, values):
        q = Query.into(trades_table)\
            .columns(*trades_columns)\
            .insert(*values)
        print(str(q))
        return self.execute_statement(str(q))

    def store_values(self, values):
        q = Query.into(values_table)\
            .columns(*values_columns)\
            .insert(*values)
        print(str(q))
        return self.execute_statement(str(q))

    def clear_values(self):
        try:
            c = self.conn.cursor()
            c.execute(clear_values)
        except Exception as e:
            print("query exception: " + str(e))
            self.close()

    def clear_trades(self):
        try:
            c = self.conn.cursor()
            c.execute(clear_trades)
        except Exception as e:
            print("query exception: " + str(e))
            self.close()

    def query_values(self):
        try:
            c = self.conn.cursor()
            c.execute(select_values)
            rows = c.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print("query exception: " + str(e))
            self.close()

    def query_trades(self):
        try:
            c = self.conn.cursor()
            c.execute(select_trades)
            rows = c.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print("query exception: " + str(e))
            self.close()


def main():
    db = DataBase()

    try:
        # create tables if not exist
        db.execute_statement(sql_create_values_table)
        db.execute_statement(sql_create_trades_table)
        db.query_values()
        db.query_trades()
    finally:
        db.close()


if __name__ == '__main__':
    main()

