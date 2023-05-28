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
from app.database import get_database ,get_collection

collection=get_collection()

router = APIRouter(prefix='/api',tags=['retrieve air pollution record'])
air_repository = AirRepository(database=get_database())



@router.get("/air", response_description="List all records")
async def get_air_pollution_record():
        air_data = await collection.find().to_list(1000)
        return air_data
        # fname = str(datetime.utcnow())
        # fname = "{}.json".format(fname)
        # print("*********************** GB *************")
        # print(fname)
        # print("*********************** GB *************")
        # # return jsonify({'airs': fname}), 200

        # # Create the list of air from our data
        # airs = await db["air"].find()

        # air_schema = AirModel(many=True)
        # output = air_schema.dump(airs).data
        # print(type(output))
        # print(output[0])
        # num_of_records = len(output)
        # print(num_of_records)
        # if (num_of_records > 100):
        #     fname = datetime.utcnow()
        #     json_fname = "{}.json".format(fname)
        #     json_fname = json_fname.replace(" ", "_")
        #     print("I AM HERE")
        #     print(json_fname)
        #     json_file_with_dir_name = "{}/{}".format(app.config["CLIENT_CSVS"], json_fname)
        #     print("*********************** GB *************")
        #     print(json_fname)
        #     print(json_file_with_dir_name)
        #     print("*********************** GB *************")

        #     csv_fname = "{}.csv".format(fname)
        #     csv_fname = csv_fname.replace(" ", "_")
        #     csv_file_with_dir_name = "{}/{}".format(app.config["CLIENT_CSVS"], csv_fname)
        #     print("*********************** GB *************")
        #     print(csv_fname)
        #     print(csv_file_with_dir_name)
        #     print("*********************** GB *************")
        #     csv_columns = ["air_id", "timestamp", "city", "state", "country", "zipcode", "place", "details", "misc",
        #                    "tVOC", "eCO2", "temp", "pressure", "altitude", "humidity", "mq2_smoke_ppm", "mq4_ng_ppm",
        #                    "mq6_lpg_ppm", "mq7_co_ppm", "mq131_o3_ppm", "co2_ppm", "dustDensity"]
        #     with open(csv_file_with_dir_name, 'a+') as outfile:
        #         wr = csv.DictWriter(outfile, fieldnames=csv_columns, dialect='excel')
        #         wr.writeheader()
        #         for record in output:
        #             wr.writerow(record)

        #     with open(json_file_with_dir_name, 'a+') as outfile:
        #         outfile.write(json.dumps(output))
        #         outfile.write("\n")

        #     csv_url = "{}/downloads/{}".format(request.url, csv_fname)
        #     json_url = "{}/downloads/{}".format(request.url, json_fname)
        #     message = ("Your query resulted in {} records. "
        #                "This is too much data to embed in this result. "
        #                "Please download the json file pasting this url in the browser: "
        #                "{}"
        #                " Or, download the file in csv format by pasting this link in the browser: "
        #                "{}"
        #                ).format(num_of_records, json_url, csv_url)
        #     return jsonable_encoder({'airs': message}), 200
        # else:
        #     return jsonable_encoder({'airs': output}), 200

        #return jsonable_encoder({'airs': "Data has been saved on server"}), 200