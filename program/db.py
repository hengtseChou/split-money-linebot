import pymongo
from datetime import datetime, timedelta
from program.config import MONGO_URL

class Mongo_object(object):

    def __init__(self):

        client = pymongo.MongoClient(MONGO_URL, connect=False)
        db = client["money_bot"]
        self.collection = db["records"]

    def insert_new(self, payer, item, amount):

        now_time_gmt_plus_8 = datetime.now() + timedelta(hours=8)
        date = now_time_gmt_plus_8.strftime("%m/%d")
        new_insert = {'date':date, 'payer':payer, 'item': item, 'amount': amount}
        x = self.collection.insert_one(new_insert)
        return x
    
    def clear(self):

        self.drop()
    
    def two_sum_difference(self):

        pipeline1 = [
            {'$match': {'payer': 'hank'}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]

        pipeline2 = [
            {'$match': {'payer': 'lala'}},
            {'$group': {'_id': None, 'total': {'$sum': '$amount'}}}
        ]

        return
    
    def print_records(self):
        
        return

Mongo = Mongo_object()
