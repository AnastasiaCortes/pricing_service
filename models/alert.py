import uuid
from typing import List

from common.database import Database
from models.item import Item


class Alert:
    def __init__(self, item_id: str, price_limit: float, _id: str = None):
        self.item_id = item_id
        self.item =Item.get_by_id(item_id)
        self.price_limit = price_limit
        self.collections = 'alerts'
        self._id = _id or uuid.uuid4().hex


    def json(self) -> dict:
        return {
            '_id': self._id,
            'price_limit': self.price_limit,
            'item_id': self.item_id
        }

    def save_to_mongo(self):
        Database.insert(self.collections, self.json())

    def load_item_price(self):
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f'Item {self.item} has reached a price under {self.price_limit}. Latest price: {self.item.price}')

    @classmethod
    def all(cls) -> List:
        alerts_from_db = Database.find('alerts', {})
        return [cls(**alert) for alert in alerts_from_db]
