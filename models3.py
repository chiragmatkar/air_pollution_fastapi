from pydantic import BaseModel 
from pydantic_mongo import AbstractRepository, ObjectIdField 
from pymongo import MongoClient 
from typing import List
import os
from bson.json_util import dumps ,default
from fastapi import Response

from fastapi.responses import  JSONResponse

class Foo(BaseModel):
    count: int
    size: float = None

class Bar(BaseModel):
    apple = 'x'
    banana = 'y'

class Spam(BaseModel):
    id: ObjectIdField = None
    foo: Foo
    bars: Bar

    class Config:
        # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectIdField: str}

class SpamRepository(AbstractRepository[Spam]):
    class Meta:
        collection_name = os.environ["MONGODB_COLLECTION"]
        model=Foo

client = MongoClient(os.environ["MONGODB"])
database = client[os.environ["MONGODB_DATABASE"]]
spam_repository = SpamRepository(database=database)

#spam = Spam(foo=Foo(count=20, size=20.0),bars=Bar(apple='i',banana='o'))


# Insert / Update
#spam_repository.save(spam)

# Delete
#spam_repository.delete(spam)

# Find One By Id
#result = spam_repository.find_one_by_id(id='64719b62611bcbd20ccbd6a9')
#print(result)

# Find One By Id using string if the id attribute is a ObjectIdField
##result = spam_repository.find_one_by({"foo.count":2})
#result = spam_repository.find_one_by(foo=Foo(count=2))
#air_repository
##result= spam_repository.find_by(list=100)
#print(result)
# Find One By Query
result = spam_repository.find_by({'foo.count': 2})
print(dumps(result))


# Find By Query
#results = spam_repository.find_by({'foo.count': {'$gte': 1}})
#print(dumps(results))

