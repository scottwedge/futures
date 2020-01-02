import requests
import json
from bs4 import BeautifulSoup
from db import DataBase
import time

levels = ["Pivot Point 2nd Level Resistance",
          "Pivot Point 1st Resistance Point",
          "Pivot Point 1st Support Point",
          "Pivot Point 2nd Support Point"]
points = ["Pivot Point"]

dbTableColumn = {"Pivot Point 1st Resistance Point": 0,
                 "Pivot Point 2nd Level Resistance": 1,
                 "Pivot Point": 2,
                 "Pivot Point 1st Support Point": 3,
                 "Pivot Point 2nd Support Point": 4}


def main():
    html = requests.get("https://www.barchart.com/futures/quotes/ESM19/cheat-sheet")

    soup = BeautifulSoup(html.text, features="html.parser")

    data = soup.find('cheat-sheet').attrs["data-cheat-sheet-data"]
    # print(data)
    # print()
    # print(json.dumps(json.loads(data), sort_keys=True, indent=4))

    raw_data = json.loads(data)
    db_data = [0, 0, 0, 0, 0]
    for obj in raw_data:
        level = obj["labelSupportResistance"]
        point = obj["labelTurningPoints"]
        if level in levels:
            db_data[dbTableColumn[level]] = obj["rawValue"]
        elif point in points:
            db_data[dbTableColumn[point]] = obj["rawValue"]

    store_values(db_data)

    # want to create trade and a sell at the first points around the pivot
    store_trades(["buy", db_data[3], 1])
    time.sleep(1)
    store_trades(["sell", db_data[0], 1])


def store_values(data):
    db = DataBase()

    try:
        print(db.store_values(data))
        db.query()
    finally:
        db.close()


def store_trades(data):
    db = DataBase()

    try:
        print(db.store_trade(data))
        db.query()
    finally:
        db.close()


if __name__ == '__main__':
    main()
