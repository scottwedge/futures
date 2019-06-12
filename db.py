import sqlite3
from pypika import Query

# database has two tables to store historical values and actions
# table name: SP_500_e_mini
# columns: date, resistance_1, resistance_2, pivot, support_1, support_2
# table name: trades
# columns: date, type, price, test, successful

dbLocation = "/Users/EvanWhite/futures.db"

values_table = "sp_500_e_mini_new"
values_columns = ["resistance_1",
                  "resistance_2",
                  "pivot",
                  "support_1",
                  "support_2"]
trades_table = "trades"
trades_columns = ["type", "price", "test"]


sql_create_values_table = """ CREATE TABLE IF NOT EXISTS SP_500_e_mini (
                                        date INTEGER PRIMARY KEY NOT NULL DEFAULT (julianday('now')),
                                        resistance_1 REAL,
                                        resistance_2 REAL,
                                        pivot REAL,
                                        support_1 REAL,
                                        support_2 REAL 
                                    ); """

sql_create_trades_table = """ CREATE TABLE IF NOT EXISTS trades (
                                        date TEXT PRIMARY KEY NOT NULL DEFAULT (datetime('now')),
                                        type INTEGER,
                                        price REAL,
                                        test INTEGER
                                    ); """

sql_insert_values = """ INSERT INTO SP_500_e_mini (resistance_1, resistance_2, pivot, support_1, support_2) 
                            VALUES (
                            :'Pivot Point 1st Resistance Point', 
                            :'Pivot Point 2nd Level Resistance', 
                            :'Pivot Point', 
                            :'Pivot Point 1st Support Point', 
                            :'Pivot Point 2nd Support Point'); """

select_values = """ SELECT * FROM SP_500_e_mini_new;"""

sql_insert_trade = """ INSERT INTO trades (type, price, test) VALUES (?, ?, ?); """

select_trades = """ SELECT * FROM trades; """


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

    def query(self):
        try:
            c = self.conn.cursor()
            c.execute(select_values)
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
        # db.execute_statement(sql_create_values_table)
        # db.execute_statement("DROP TABLE trades;")
        # db.execute_statement(sql_create_trades_table)
        db.query()
    finally:
        db.close()


if __name__ == '__main__':
    main()

