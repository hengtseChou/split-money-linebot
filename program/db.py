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
        if payer == 'hank':
            new_insert = {'date':date, 'item': item, 'hank': int(amount), 'lala':0}
        elif payer == 'lala':
            new_insert = {'date':date, 'item': item, 'hank': 0, 'lala': int(amount)}
        x = self.collection.insert_one(new_insert)
        return x
    
    def clear(self):

        self.collection.drop()
    
    def two_sum_difference(self):

        sum_values = []

        for payer in ['hank', 'lala']:
            pipeline = [
                {'$group': {'_id': None, 'total': {'$sum': '$'+payer}}}
            ]
            result = list(self.collection.aggregate(pipeline))
            if not result:
                sum_values.append(0)
            else:
                sum_values.append(result[0]['total'])

        if sum_values[0] > sum_values[1]:
            pays_more = 'hank'
        elif sum_values[0] < sum_values[1]:
            pays_more = 'lala'
        else:
            pays_more = 'no_one'       

        return pays_more, abs(sum_values[0] - sum_values[1])
    
    def find_all(self):
        
        cursor = self.collection.find({}, {'_id': 0})
        return cursor

Mongo = Mongo_object()
