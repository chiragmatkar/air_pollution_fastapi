from pydantic import BaseModel,validator , Field
from typing import Optional , List , Dict
from pydantic_mongo import AbstractRepository, ObjectIdField 
from pymongo import MongoClient 
from bson import ObjectId
import os



class Location(BaseModel):
    zipcode: int
    city:  str 
    state: str
    country:  str
    zipcode: str
    place:  str
    details:  str
    misc:  str


class Environment(BaseModel):
    tVOC : float 
    eCO2 : float 
    temp : float 
    pressure : float 
    altitude : float 
    humidity : float 

class MQ2(BaseModel):
    mq2_raw: float 
    mq2_ro : float 
    mq2_rs_by_ro : float 
    mq2_lpg_ppm : float 
    mq2_co_ppm : float 
    mq2_smoke_ppm : float 
    mq2_ref_ro : float 
    mq2_ref_lpg_ppm : float 
    mq2_ref_co_ppm : float 
    mq2_ref_smoke_ppm : float 


class MQ4(BaseModel):
    mq4_raw: float 
    mq4_ro : float 
    mq4_rs_by_ro: float 
    mq4_ng_ppm : float 
    mq4_ng_ppm2 : float 
    mq4_ref_ro : float 
    mq4_ref_ng_ppm : float 


class MQ6(BaseModel):
    mq6_raw : float 
    mq6_ro : float 
    mq6_rs_by_ro : float  
    mq6_lpg_ppm : float 
    mq6_lpg_ppm2 : float  
    mq6_ref_ro : float 
    mq6_ref_lpg_ppm : float 


class MQ7(BaseModel):
    mq7_raw : float 
    mq7_ro : float 
    mq7_rs_by_ro : float 
    mq7_co_ppm : float 
    mq7_h2_ppm : float 
    mq7_co_ppm2 : float 
    mq7_ref_ro : float 
    mq7_ref_co_ppm : float 
    mq7_ref_h2_ppm : float 


class MQ131(BaseModel):
    mq131_raw : float 
    mq131_ro : float 
    mq131_rs_by_ro : float 
    mq131_o3_ppm : float 
    mq131_o3_ppm2 : float 
    mq131_ref_ro : float 
    mq131_ref_o3_ppm :float  

class CO2(BaseModel):
    # CO2 sensor
    co2_raw : float 
    co2_ppm : float 

class Dust(BaseModel):
    dust_raw : float 
    dust_Vo : float 
    dust_Voc : float 
    dust_dV : float 
    dust_Vo_mV : float 
    dustDensity : float 


class Air(BaseModel):
    id: ObjectIdField = None
    locationDetails : List[Location]
    env : List[Environment]
    mq2 : List[MQ2]
    mq4 : List[MQ4]
    mq6 : List[MQ6]
    mq7 : List[MQ7]
    mq131 : List[MQ131]
    co2 : List[CO2]
    dust : List[Dust]

    class Config:
        # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectIdField: str}

class AirRepository(AbstractRepository[Air]):
    class Meta:
        collection_name = os.environ["MONGODB_COLLECTION"]


air = Air(locationDetails=Location((zipcode=400001,city="Mubai",state="Maharashtra",country="India",place="Bhandup",details="LBS Road",misc="OppJain Mandir"),
          env=(tVOC=3.2,eCO2)
          ))

air = Air(locationDetails=[{
        "zipcode":400001,
        "city":"Mumbai",
        "state":"Maharashtra",
        "country":"India",
        "place":"Bhandup",
        "details":"LBS Road",
        "misc":"Opp Jain Mandir"}],
        env=[{
        "tVOC": 3.2,
                    "eCO2": 2.0,
                    "temp": 37.2,
                    "pressure": 24.2,
                    "altitude": 2.1,
                    "humidity": 9.0    

        }],
          mq2=[{
               "mq2_raw" : 3.2,
                    "mq2_ro" : 1.2,
                    "mq2_rs_by_ro" : 9.2,
                    "mq2_lpg_ppm" : 6.2,
                    "mq2_co_ppm" : 5.0,
                    "mq2_smoke_ppm" : 2.0,
                    "mq2_ref_ro" : 3.9,
                    "mq2_ref_lpg_ppm" : 7.9 , 
                    "mq2_ref_co_ppm" : 5.0,
                    "mq2_ref_smoke_ppm" : 6.0,
          }],
          mq4=[{
               "mq4_raw" : 6.0,
                     "mq4_ro" : 6.0,
                     "mq4_rs_by_ro" : 6.0,
                     "mq4_ng_ppm" : 6.0,
                    "mq4_ng_ppm2" : 6.0,
                    "mq4_ref_ro" : 6.0,
                     "mq4_ref_ng_ppm" : 6.0,

          }],
          mq6=[{
              "mq6_raw" : 6.0,
                    "mq6_ro" : 6.0,
                    "mq6_rs_by_ro" : 6.0,
                    "mq6_lpg_ppm" : 6.0,
                    "mq6_lpg_ppm2" : 6.0,
                    "mq6_ref_ro" : 6.0,
                    "mq6_ref_lpg_ppm" : 6.0,

          }],
          mq7=[{
              
                # MQ7 - CO
                    "mq7_raw" : 6.0,
                    "mq7_ro" : 6.0,
                    "mq7_rs_by_ro" : 6.0,
                    "mq7_co_ppm" : 6.0,
                    "mq7_h2_ppm" : 6.0,
                    "mq7_co_ppm2" : 6.0,
                    "mq7_ref_ro" : 6.0,
                    "mq7_ref_co_ppm" : 6.0,
                    "mq7_ref_h2_ppm" : 6.0,
          }],
          mq131=[{
    "mq131_raw" : 6.0 ,
    "mq131_ro" : 6.0 ,
    "mq131_rs_by_ro" : 6.0 ,
    "mq131_o3_ppm" : 6.0 , 
    "mq131_o3_ppm2" : 6.0 ,
    "mq131_ref_ro" : 6.0 ,
    "mq131_ref_o3_ppm" :6.0  
          }],
          co2=[{
              "co2_raw" : 6.0,
                    "co2_ppm" : 6.0,

          }],
          dust=[{
               "dust_raw" : 6.0,
                    "dust_Vo": 6.0,
                    "dust_Voc" : 6.0,
                    "dust_dV" : 6.0,
                    "dust_Vo_mV" : 6.0,
                    "dustDensity" : 6.0,

          }]
          )


def get_database():
    client = MongoClient(os.environ["MONGODB_URL"])
    database = client[os.environ["MONGODB_DATABASE"]]
    return database

# air_repository = AirRepository(database=database)

# # Insert / Update
# air_repository.save(air)
# result = air_repository.find_one_by_id(air.id)
# print(air.id)
# print(result)

# result2 = air_repository.find_one_by({'zipcode': 400001})
# print(result2)