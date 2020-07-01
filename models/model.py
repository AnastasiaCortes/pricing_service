from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Type

from common.database import Database

T = TypeVar('T', bound="Model")  # custom type variable - T must be a Model, or subclass of a Model, nothing else


class Model(metaclass=ABCMeta):
    # this gonna exist but don't have value yet
    collection: str
    _id: str

    # class properties can be accessed as instance as well ( self.)

    def __init__(self, *args, **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {'_id': self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {'_id': self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:  # returning an object
        return cls.find_one_by("_id", _id)

    @abstractmethod
    def json(self) -> dict:
        raise NotImplementedError

    @classmethod
    def all(cls) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**element) for element in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: str) -> T:  # Item.find_one_by('url', 'http://bla.com'
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: str) -> List[T]:
        return [cls(**element) for element in Database.find(cls.collection, {attribute: value})]
