from peewee import *

db = SqliteDatabase('inventory.db')
costdb = SqliteDatabase('Costs.db')

class Entry(Model):
    name = TextField()
    size = FloatField()
    purchaseCost = FloatField()
    purchaseDate = DateTimeField()
    soldCost = FloatField()
    soldDate = DateTimeField()
    soldLocation = TextField()

    class Meta:
        database = db

class Cost(Model):
    what = TextField()
    cost = FloatField()
    purchaseDate = DateTimeField()

    class Meta:
        database = costdb

def init():
    """create datebase/table if they dont exist"""
    db.connect()
    db.create_tables([Entry], safe=True)

    costdb.connect()
    costdb.create_tables([Cost], safe=True)