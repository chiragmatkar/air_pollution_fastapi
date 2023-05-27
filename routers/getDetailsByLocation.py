from fastapi import APIRouter
from fastapi import  Body,  status
from models import AirModel , AirRepository
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
import os
from functions.variables import *
from functions.calculate_on_ref_Ro import calculate_on_ref_Ro, create_datetime_obj
import csv
import json
from datetime import datetime
from typing import List
from database import get_database ,get_collection
import json
from bson import ObjectId

router = APIRouter(prefix='/api',tags=['get air pollution record by location'])
air_repository = AirRepository(database=get_database())
collection=get_collection()


@router.get("/air/country/{country}", response_description="List all records created for country")
async def get_record_by_country(country):
        air_data=fetch_by_country(country)
        #air_data = await collection.find_one({"country": str(country)})
        if(air_data):
                return air_data
        else:
                return {"log":"No Country record found"}


@router.get("/air/country/{country}/state/{state}", response_description="List all records created after for state", response_model=AirModel)
async def get_record_by_state(country,state):
             air_data = await collection.find_one({"country": str(country),"state": str(state)})
             if(air_data):
                return air_data
             else:
                return {"log":"No State record found"}
 
@router.get("/air/country/{country}/state/{state}/city/{city}", response_description="List all records created before date", response_model=AirModel)
async def get_record_by_city(country,state,city):
        air_data = await collection.find_one({"country" : country ,"state": str(state),"city": str(city)})
        if(air_data):
                return air_data
        else:
                return {"log":"No City record found"}


async def fetch_by_country(country:str):
        list = []  
        cursor = collection.find({"name":country})
        for document in cursor:
                list.append(document)
        return list