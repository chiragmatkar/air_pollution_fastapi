from variables import * 
from datetime import date, datetime, timedelta
from apps.graph import timeseries_graphs
from models import Air, AirSchema
from variables import *
from functions.calculate_on_ref_Ro import *



def cumulative_exposure_data(zipcode):
    # past_8_hours = cumulative_data(zipcode, 22)
    past_8_hours = cumulative_data(zipcode, 8)
    past_24_hours = cumulative_data(zipcode, 24)
    past_week = cumulative_data(zipcode, 168)

    data_pm25 = {
        "name": ABBR_PM25,
        "unit": UNITS_PM25,
        "order": 1,
        "stats": [
            {
                "title": "8 Hours",
                "order": 1,
                "stats": past_8_hours["avg_pm25"]
            },
            {
                "title": "24 Hours",
                "order": 2,
                "stats": past_24_hours["avg_pm25"]
            },
            {
                "title": "1 week",
                "order": 3,
                "stats": past_week["avg_pm25"]
            }
        ]
    }

    data_tVOC = {
        "name": ABBR_TVOC,
        "unit": UNITS_TVOC,
        "order": 2,
        "stats": [
            {
                "title": "8 Hours",
                "order": 1,
                "stats": past_8_hours["avg_tVOC"]
            },
            {
                "title": "24 Hours",
                "order": 2,
                "stats": past_24_hours["avg_tVOC"]
            },
            {
                "title": "1 week",
                "order": 3,
                "stats": past_week["avg_tVOC"]
            }
        ]
    }

    data_co2 = {
        "name": ABBR_CO2,
        "unit": UNITS_CO2,
        "order": 3,
        "stats": [
            {
                "title": "8 Hours",
                "order": 1,
                "stats": past_8_hours["avg_co2"]
            },
            {
                "title": "24 Hours",
                "order": 2,
                "stats": past_24_hours["avg_co2"]
            },
            {
                "title": "1 week",
                "order": 3,
                "stats": past_week["avg_co2"]
            }
        ]
    }

    data_o3 = {
        "name": ABBR_O3,
        "unit": UNITS_O3,
        "order": 4,
        "stats": [
            {
                "title": "8 Hours",
                "order": 1,
                "stats": past_8_hours["avg_o3"]
            },
            {
                "title": "24 Hours",
                "order": 2,
                "stats": past_24_hours["avg_o3"]
            },
            {
                "title": "1 week",
                "order": 3,
                "stats": past_week["avg_o3"]
            }
        ]
    }

    average_exposure = {
        "averageExposure": [data_pm25, data_tVOC, data_co2, data_o3]
    }

    return average_exposure





def cumulative_data(zipcode, num_of_hours):
    past_time = datetime.now() - timedelta(hours=num_of_hours)

    # t1 = time.time()
    airdata = Air.query.with_entities(
        func.avg(Air.dustDensity).label('avg_pm25'),
        func.avg(Air.tVOC).label('avg_tVOC'),
        func.avg(Air.co2_ppm).label('avg_co2'),
        func.avg(Air.mq131_o3_ppm).label('avg_o3')
    ).filter(Air.zipcode == zipcode, Air.timestamp >= past_time).all()

    # t2 = time.time()
    if not airdata:
        data = {
            "avg_pm25": "N/A",
            "avg_tVOC": "N/A",
            "avg_co2": "N/A",
            "avg_o3": "N/A"
        }
        return data

    air_aggrs = airdata[0]

    if not air_aggrs:
        data = {
            "avg_pm25": "N/A",
            "avg_tVOC": "N/A",
            "avg_co2": "N/A",
            "avg_o3": "N/A"
        }
        return data
    else:
        if air_aggrs[0]:
            val_pm25 = round(air_aggrs[0], 2)
        else:
            val_pm25 = "N/A"

        if air_aggrs[1]:
            val_tVOC = round(air_aggrs[1], 2)
        else:
            val_tVOC = "N/A"

        if air_aggrs[2]:
            val_co2 = round(air_aggrs[2], 2)
        else:
            val_co2 = "N/A"

        if air_aggrs[3]:
            val_o3 = round(air_aggrs[3], 2)
        else:
            val_o3 = "N/A"

    # t3 = time.time()
    data = {
        "avg_pm25": val_pm25,
        "avg_tVOC": val_tVOC,
        "avg_co2": val_co2,
        "avg_o3": val_o3
    }
    # print (data)
    return data




def ORIGINAL_SUMMARY_cumulative_data(zipcode, num_of_days):
    past_time = datetime.now() - timedelta(days=num_of_days)

    # t1 = time.time()
    airdata = Air.query.with_entities(
        func.sum(Air.dustDensity).label('avg_pm25'),
        func.sum(Air.tVOC).label('avg_tVOC'),
        func.sum(Air.co2_ppm).label('avg_co2'),
        func.sum(Air.mq131_o3_ppm).label('avg_o3')
    ).filter(Air.zipcode == zipcode, Air.timestamp >= past_time).all()

    # t2 = time.time()
    if not airdata:
        return {}

    air_aggrs = airdata[0]

    # t3 = time.time()
    data = {
        "total_pm25": air_aggrs[0],
        "total_tVOC": air_aggrs[1],
        "total_co2": air_aggrs[2],
        "total_o3": air_aggrs[3]
    }
    # print (data)
    return data
