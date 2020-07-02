import re
import uuid
from dataclasses import dataclass, field
from models.model import Model


@dataclass(eq=False)
class Store(Model):
    name: str
    url_prefix: str
    tag_name: str
    query: dict
    collection: str = field(default="stores", init=False)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex )

    def json(self) -> dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, sore_name: str) -> "Store":
        return cls.find_one_by("name", sore_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)") # gives first part of url
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
