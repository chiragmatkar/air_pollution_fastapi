from fastapi import APIRouter
from fastapi import  Body,  status
from models import AirModel , AirRepository
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
import os
#from functions.cumulative_data import cumulative_exposure_data
#from functions.timeseries import timeseries_data
from datetime import datetime
from typing import List
from database import get_database


router = APIRouter(prefix='/api',tags=['get air pollution record by atomosme'])
air_repository = AirRepository(database=get_database())



@router.get("/air/zipcode/{zipcode}/atomosome/summary", response_description="atmosome summary data")
def atmosome_data_summary(zipcode):
    # data = hourly_data(zipcode)
    # data = hourly_data(zipcode, 720)s
    return {"status":"success"}

'''

'''
@router.get("/air/zipcode/{zipcode}/atomosome", response_description="atmosome entire data")
async def atmosome_data(zipcode):
       # hourly_info = hourly_data(zipcode, 720)
        #hourly_info = hourly_data(zipcode)
        #cumulative_info = cumulative_exposure_data(zipcode)
        #timeseries_info = timeseries_data(zipcode)

        data = {}
        #data.update(hourly_info)
        #data.update(cumulative_info)
        #data.update(timeseries_info)

        return JSONResponse(status_code=status.HTTP_200_OK, content=data)
 


'''
Atmosome Cumulative Data
'''
# @router.get("/api/air/zipcode/{zipcode}/atmosome/cumulative", response_description="atmosome cumulative")
# async def atmosome_data_cumulative(zipcode):
#     data = cumulative_exposure_data(zipcode)
#     return data

# '''
# Atmosome Timeseries Data
# '''
# @router.get("/api/air/zipcode/{zipcode}/atmosome/timeseries", response_description="atmosome cumulative")
# def atmosome_data_timeseries(zipcode):
#     data = timeseries_data(zipcode)
#     return data