from pydantic import BaseModel, Field, EmailStr ,validator 
from bson import ObjectId
from typing import Optional
from datetime import datetime
from pydantic_mongo import AbstractRepository, ObjectIdField 
import os

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    @validator("status")
    def replace_none(cls, v):
        return v or "None"

class AirModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
         
    #Geographic
    city:  Optional[str]  
    state: Optional[str] 
    country: Optional[str] 
    zipcode: Optional[int] 
    place: Optional[str] 
    details: Optional[str] 
    misc: Optional[str] 

    # Environmental
    tVOC : Optional[float] 
    eCO2 : Optional[float] 
    temp : Optional[float] 
    pressure : Optional[float] 
    altitude : Optional[float] 
    humidity : Optional[float] 


    # MQ2
    mq2_raw: Optional[float] 
    mq2_ro : Optional[float] 
    mq2_rs_by_ro : Optional[float] 
    mq2_lpg_ppm : Optional[float] 
    mq2_co_ppm : Optional[float] 
    mq2_smoke_ppm : Optional[float] 
    mq2_ref_ro : Optional[float] 
    mq2_ref_lpg_ppm : Optional[float] 
    mq2_ref_co_ppm : Optional[float] 
    mq2_ref_smoke_ppm : Optional[float] 

      # MQ4 - Natural gas
    mq4_raw : Optional[float] 
    mq4_ro : Optional[float] 
    mq4_rs_by_ro : Optional[float] 
    mq4_ng_ppm : Optional[float] 
    mq4_ng_ppm2 : Optional[float] 
    mq4_ref_ro : Optional[float] 
    mq4_ref_ng_ppm : Optional[float] 
    # MQ6 - LPG
    mq6_raw : Optional[float] 
    mq6_ro : Optional[float] 
    mq6_rs_by_ro : Optional[float] 
    mq6_lpg_ppm : Optional[float] 
    mq6_lpg_ppm2 : Optional[float] 
    mq6_ref_ro : Optional[float] 
    mq6_ref_lpg_ppm : float 
    # MQ7 - CO
    mq7_raw : float 
    mq7_ro : float 
    mq7_rs_by_ro : float 
    mq7_co_ppm : float 
    mq7_h2_ppm : float 
    mq7_co_ppm2 : float 
    mq7_ref_ro : float 
    mq7_ref_co_ppm : float 
    mq7_ref_h2_ppm : float 
    # MQ131 - Ozone
    mq131_raw : float 
    mq131_ro : float 
    mq131_rs_by_ro : float 
    mq131_o3_ppm : float 
    mq131_o3_ppm2 : float 
    mq131_ref_ro : float 
    mq131_ref_o3_ppm :float 
    # CO2 sensor
    co2_raw : float 
    co2_ppm : float 
    # PM 2.5/dust sensor
    dust_raw : float 
    dust_Vo : float 
    dust_Voc : float 
    dust_dV : float 
    dust_Vo_mV : float 
    dustDensity : float 

    class Config:
        allow_population_by_field_name : True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {        
                    "city": "Mumbai",
                    "state": "Maharashtra",
                    "country": "India",
                    "zipcode": 400043,
                    "place": "Bhandup",
                    "details": "Opp Jain Mandir",
                    "misc": "Gate Pass required",    
                   
                    "tVOC": 3.2,
                    "eCO2": 2.0,
                    "temp": 37.2,
                    "pressure": 24.2,
                    "altitude": 2.1,
                    "humidity": 9.0,
                    #m2
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
                    #m4
                     "mq4_raw" : 6.0,
                     "mq4_ro" : 6.0,
                     "mq4_rs_by_ro" : 6.0,
                     "mq4_ng_ppm" : 6.0,
                    "mq4_ng_ppm2" : 6.0,
                    "mq4_ref_ro" : 6.0,
                     "mq4_ref_ng_ppm" : 6.0,
                     # MQ6 - LPG
                    "mq6_raw" : 6.0,
                    "mq6_ro" : 6.0,
                    "mq6_rs_by_ro" : 6.0,
                    "mq6_lpg_ppm" : 6.0,
                    "mq6_lpg_ppm2" : 6.0,
                    "mq6_ref_ro" : 6.0,
                    "mq6_ref_lpg_ppm" : 6.0,
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
                      # MQ131 - Ozone
                    "mq131_raw"  : 6.0,
                    "mq131_ro" : 6.0,
                    "mq131_rs_by_ro": 6.0,
                    "mq131_o3_ppm" : 6.0,
                    "mq131_o3_ppm2" : 6.0,
                    "mq131_ref_ro" : 6.0,
                    "mq131_ref_o3_ppm": 6.0,

                    # CO2 sensor
                    "co2_raw" : 6.0,
                    "co2_ppm" : 6.0,
                    # PM 2.5/dust sensor
                    "dust_raw" : 6.0,
                    "dust_Vo": 6.0,
                    "dust_Voc" : 6.0,
                    "dust_dV" : 6.0,
                    "dust_Vo_mV" : 6.0,
                    "dustDensity" : 6.0,
           
            }
        }

class AirRepository(AbstractRepository[AirModel]):
    class Meta:
        collection_name = os.environ["MONGODB_COLLECTION"]

class UpdateAirModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }



def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }