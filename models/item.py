import uuid
from typing import Dict
import requests
from bs4 import BeautifulSoup
import re
from models.model import Model
from dataclasses import dataclass, field

@dataclass(eq=False)
class Item(Model):
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    collection: str = field(default='items', init=False)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex )

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()  # ex "$1,234.00"

        pattern = re.compile(r'(\d+,?\d*\.\d\d)')
        match = pattern.search(string_price)
        found_price = match.group(1)  # ex "1,234.00"
        without_commas = found_price.replace(',', '')  # "1234.00"
        self.price = float(without_commas)  # 1234.0
        return self.price

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'url': self.url,
            'tag_name': self.tag_name,
            'price': self.price,
            'query': self.query
        }






