from fastapi import APIRouter
from fastapi import  Body,  status , Depends
from app.models import AirModel , AirRepository
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
import os
from app.functions.variables import *
from app.functions.calculate_on_ref_Ro import calculate_on_ref_Ro, create_datetime_obj
import csv
import json
from datetime import datetime
from typing import List
from app.database import get_database ,get_collection

router = APIRouter(prefix='/api',tags=['get air pollution record by zipcode'])
air_repository = AirRepository(database=get_database())
collection=get_collection()



@router.get("/air/zipcode/{zipcode}", response_description="Zip Code details recieved")
async def get_data_by_zipcode(zipcode):
            air_data = await collection.find_one({"zipcode": int(zipcode)})
            return air_data    
    

@router.get("/air/zipcodes", response_description="Records with distinct zipcode")
async def get_by_distinct_zipcode():
        air_data = await collection.distinct("zipcode")
        return {"zipcodes" : air_data}


@router.get("/air/zipcodes/{zipcode}/pollutants", response_description="Pollutants data in zipcode")
async def data_pollutants_by_zipcode(zipcode):
        air_data = await collection.find_one({"zipcode": int(zipcode)})
        if(air_data):
                return { "metrics" : { "temperature": air_data['temp'],
                               "pressure": air_data['pressure'],
                                "altitude": air_data['altitude'],
                                "humidity": air_data['humidity'],
                                "city": air_data['city'],
                                "state": air_data['state'],
                                "country": air_data['country'],
                              
                              },
                               "pollutants" : {
                                 "tVOC": air_data['tVOC'],
                                 "eCO2": air_data['eCO2'],
        #                         "smoke": air_data['smoke'],
        #                         "ng": air_data['ng'],
        #                         "lpg": air_data['lpg'],
        #                         "co": air_data['co'],
        #                         "h2": air_data['h2'],
        #                         "o3": air_data['o3'],
        #                         "co2": air_data['co2'],
         #                       "pm2.5": air_data['pm2.5'],
         }
                              }
        else:
                return {"status" : "No records found"}
        
