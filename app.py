from flask import Flask
from models.item import Item
from models.alert import Alert

URL ='https://www.johnlewis.com/2020-apple-ipad-pro-12-9-inch-a12z-bionic-ios-wi-fi-256gb/space-grey/p4949087'
TAG_NAME = 'p'
QUERY ={'class': 'price price--large'}

item = Item(URL, TAG_NAME, QUERY)
item.save_to_mongo()
items_loaded = Item.all()
print(items_loaded)
print(items_loaded[0].load_price())

alert = Alert("2ea0b50674984970b01ce73885bc6ade", 2000)
alert.save_to_mongo()