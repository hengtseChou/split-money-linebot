from datetime import datetime, timedelta

from pymongo import MongoClient

from .config import ENV, MONGO_URL


def today_str(env):
    if env == "develop":
        return datetime.now().strftime("%m/%d")
    elif env == "prod":
        return (datetime.now() + timedelta(hours=8)).strftime("%m/%d")


class MongoHandler:
    def __init__(self, mongo_url) -> None:
        client = MongoClient(mongo_url, connect=False)
        db = client["money_bot"]
        self._collection = db["records"]

    @property
    def records(self):
        return self._collection

    def new_record(self, payer, amount):
        date = today_str(ENV)
        if payer == "hank":
            new_insert = {"date": date, "hank": int(amount), "lala": 0}
        elif payer == "lala":
            new_insert = {"date": date, "hank": 0, "lala": int(amount)}
        self._collection.insert_one(new_insert)

    def all_records(self):
        result = self._collection.find({}, {"_id": 0})
        return list(result)

    def clear_all(self):
        self._collection.drop()


mongo_handler = MongoHandler(MONGO_URL)
