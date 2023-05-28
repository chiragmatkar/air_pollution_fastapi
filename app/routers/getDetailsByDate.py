from fastapi import APIRouter
from fastapi import  Body,  status
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
from app.database import get_database

router = APIRouter(prefix='/api',tags=['get air pollution record by date'])
air_repository = AirRepository(database=get_database())



@router.get("/air/zipcode/{zipcode}/24hours", response_description="Zip Code details recieved in last 24 hrs",response_model=AirModel)
async def get_24hours_data_by_zipcode(zipcode):
            zipdetails = await air_repository.find().to_list(100)
            print(zipdetails)
            return zipdetails


@router.get("/air/start_date/{start_date}", response_description="List all records created after date", response_model=AirModel)
async def get_record_from_startdate(start_date):
        air_data = await db["air"].find({"created_at" : "{ $gte : new ISODate("+ start_date +")" })
        return air_data
 


@router.get("/air/end_date/{end_date}", response_description="List all records created before date", response_model=AirModel)
async def get_record_till_enddate(end_date):
        air_data = await db["air"].find({"created_at" : "{ $gte : new ISODate("+ end_date +")" })
        return air_data
 

@router.get("/air/end_date/{start_date}/{end_date}", response_description="List all records created before date", response_model=AirModel)
async def get_record_from_startdate_to_enddate(start_date,end_date):
        air_data = await db["air"].find({"created_at" : "{ $gte : new ISODate("+ start_date +" , $lte : new ISODate("+ end_date +") " })
        return air_data