import pymongo
from datetime import datetime, timedelta
from program.config import MONGO_URL

class Mongo_object(object):

    def __init__(self):

        client = pymongo.MongoClient(MONGO_URL, connect=False)
        db = client["map_bot"]
        self.collection = db["users"]

    def insert_new(self, payer, amount):

        now_time_gmt_plus_8 = datetime.now() + timedelta(hours=8)
        date = now_time_gmt_plus_8.strftime("%m/%d")
        new_insert = {'date':date, 'payer':payer, 'amount': amount}
        x = self.collection.insert_one(new_insert)
        return x