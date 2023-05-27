from fastapi import APIRouter
from fastapi import  Body,  status
from models import AirModel , AirRepository
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder
from functions.variables import *
from functions.calculate_on_ref_Ro import calculate_on_ref_Ro, create_datetime_obj
from database import get_database ,get_collection

router = APIRouter(prefix='/api',tags=['create air pollution record'])
air_repository = AirRepository(database=get_database())
collection=get_collection()

@router.post("/air", response_description="Add new air pollution record", response_model=AirModel)
async def create_air_pollution_record(air: AirModel):
    air = jsonable_encoder(air)
    date_str=air['created_at']
    
    mq2_raw = float(air['mq2_raw'])
    mq2_ref_lpg_ppm = calculate_on_ref_Ro(mq2_raw,MQ2_RL,MQ2_Ref_Ro,MQ2_LPGCurve)
    print ("mq2 LPG: old: 0 ppm new: {0:.4f} ppm".format(mq2_ref_lpg_ppm))
    mq2_ref_co_ppm = calculate_on_ref_Ro(mq2_raw,MQ2_RL,MQ2_Ref_Ro,MQ2_COCurve)
    print ("mq2 CO: old: 0 ppm new: {0:.4f} ppm".format(mq2_ref_co_ppm))
    mq2_ref_smoke_ppm = calculate_on_ref_Ro(mq2_raw,MQ2_RL,MQ2_Ref_Ro,MQ2_SmokeCurve)
    print ("mq2 SMOKE: old: 0 ppm new: {0:.4f} ppm".format(mq2_ref_smoke_ppm))

    mq4_raw = float(air['mq4_raw'])
    mq4_ref_ng_ppm = calculate_on_ref_Ro(mq4_raw,MQ4_RL, MQ4_Ref_Ro,MQ4_MethaneCurve)
    print ("mq4 NG: old: 0 ppm new: {0:.4f} ppm".format(mq4_ref_ng_ppm))

    mq6_raw = float(air['mq6_raw'])
    mq6_ref_lpg_ppm = calculate_on_ref_Ro(mq6_raw,MQ6_RL,MQ6_Ref_Ro, MQ6_LPGCurve)
    print ("mq6 LPG: old: 0 ppm new: {0:.4f} ppm".format(mq6_ref_lpg_ppm))

    mq7_raw = float(air['mq7_raw'])
    mq7_ref_co_ppm = calculate_on_ref_Ro(mq7_raw,MQ7_RL,MQ7_Ref_Ro,MQ7_COCurve)
    print ("mq7: old CO: 0 ppm new CO: {0:.4f} ppm".format(mq7_ref_co_ppm))

    mq7_ref_h2_ppm = calculate_on_ref_Ro(mq7_raw,MQ7_RL,MQ7_Ref_Ro,MQ7_H2Curve)
    print ("mq7: old H2: 0 ppm new H2: {0:.4f} ppm".format(mq7_ref_h2_ppm))

    try:
        mq131_raw = float(air['mq131'])
    except KeyError as e:
        mq131_raw = float(air['mq131_raw'])

    mq131_ref_o3_ppm = calculate_on_ref_Ro(int(mq131_raw), MQ131_RL, MQ131_Ref_Ro, MQ131_O3Curve)
    print ("mq131: old: 0 ppm new: {0:.4f} ppm".format(mq131_ref_o3_ppm))


    zipcode = int(air['zipcode'])
    altitude = float(air['altitude'])
    temp = float(air['temp'])
    mq4_ng_ppm = float(air['mq4_ng_ppm'])

    if zipcode == '94720':
            if altitude < 150:
                altitude = 177.0
            elif altitude > 210:
                altitude = 177.0
            if mq4_ng_ppm > 100:
                mq4_ng_ppm = mq4_ng_ppm / 100
    elif zipcode == '95014':
            if altitude < 180:
                altitude = 236.0
            elif altitude > 250:
                altitude = 236.0
    elif zipcode == '95064':
            if altitude < 650:
                altitude = 763.0
            elif altitude > 850:
                altitude = 763.0
            temp = temp - 5
    elif zipcode == '96150':
            if altitude < 5500:
                altitude = 6263.0
            elif altitude > 6350:
                altitude = 6263.0
    elif zipcode == '94305':
            if altitude < 135:
                altitude = 141.0
            elif altitude > 155:
                altitude = 141.0

    co2_raw = float(air['co2_raw'])
    co2_ppm = float(air['co2_ppm'])

    if zipcode == '94305':
            concentration = co2_raw * 8
            # concentration = concentration/1.5;
            if concentration < 0:
                print("Not adjusting co2ppm.")
            else:
                print("concentration: {}".format(concentration))

                if concentration > 600:
                    concentration = (concentration * 1.5) / 1.4
                elif concentration > 1000:
                    concentration = (concentration * 1.5) / 1.3

                co2_raw = co2_ppm
                co2_ppm = concentration

                print("co2_ppm: {}".format(co2_ppm))
                print("END HARI ADJUSTED BLAU LAB CO2 END")

    if date_str:
            T_idx = date_str.find("T")
            if T_idx >= 0:
                datetime_obj = create_datetime_obj(date_str, delimiter="T")
            else:
                datetime_obj = create_datetime_obj(date_str)
            print("----------Normal---------")   
            air = AirModel(
                timestamp=datetime_obj,
                city=air['city'],
                state=air['state'],
                country=air['country'],
                # zipcode=air['zipcode'],
                zipcode=zipcode,
                place=air['place'],
                details=air['details'],
                misc=air['misc'],
                tVOC=float(air['tVOC']),
                eCO2=float(air['eCO2']),
                temp=temp,
                pressure=float(air['pressure']),
                # altitude=float(air['altitude']),
                altitude=altitude,
                humidity=float(air['humidity']),
                mq2_raw=mq2_raw,
                mq2_ro=float(air['mq2_ro']),
                mq2_rs_by_ro=float(air['mq2_rs_by_ro']),
                mq2_lpg_ppm=float(air['mq2_lpg_ppm']),
                mq2_co_ppm=float(air['mq2_co_ppm']),
                mq2_smoke_ppm=float(air['mq2_smoke_ppm']),
                mq2_ref_ro=MQ2_Ref_Ro,
                mq2_ref_lpg_ppm=mq2_ref_lpg_ppm,
                mq2_ref_co_ppm=mq2_ref_co_ppm,
                mq2_ref_smoke_ppm=mq2_ref_smoke_ppm,
                mq4_raw=mq4_raw,
                mq4_ro=float(air['mq4_ro']),
                mq4_rs_by_ro=float(air['mq4_rs_by_ro']),
                # mq4_ng_ppm=float(air['mq4_ng_ppm']),
                mq4_ng_ppm=mq4_ng_ppm,
                mq4_ng_ppm2=float(air['mq4_ng_ppm2']),
                mq4_ref_ro=MQ4_Ref_Ro,
                mq4_ref_ng_ppm=mq4_ref_ng_ppm,
                mq6_raw=mq6_raw,
                mq6_ro=float(air['mq6_ro']),
                mq6_rs_by_ro=float(air['mq6_rs_by_ro']),
                mq6_lpg_ppm=float(air['mq6_lpg_ppm']),
                mq6_lpg_ppm2=float(air['mq6_lpg_ppm2']),
                mq6_ref_ro=MQ6_Ref_Ro,
                mq6_ref_lpg_ppm=mq6_ref_lpg_ppm,
                mq7_raw=mq7_raw,
                mq7_ro=float(air['mq7_ro']),
                mq7_rs_by_ro=float(air['mq7_rs_by_ro']),
                mq7_co_ppm=float(air['mq7_co_ppm']),
                mq7_h2_ppm=float(air['mq7_h2_ppm']),
                mq7_co_ppm2=float(air['mq7_co_ppm2']),
                mq7_ref_ro=MQ7_Ref_Ro,
                mq7_ref_co_ppm=mq7_ref_co_ppm,
                mq7_ref_h2_ppm=mq7_ref_h2_ppm,
                mq131_raw=mq131_raw,
                mq131_ro=float(air['mq131_ro']),
                mq131_rs_by_ro=float(air['mq131_rs_by_ro']),
                mq131_o3_ppm=float(air['mq131_o3_ppm']),
                mq131_o3_ppm2=float(air['mq131_o3_ppm2']),
                mq131_ref_ro=MQ131_Ref_Ro,
                mq131_ref_o3_ppm=mq131_ref_o3_ppm,
                # co2_raw=float(air['co2_raw']),
                # co2_ppm=float(air['co2_ppm']),
                co2_raw=co2_raw,
                co2_ppm=co2_ppm,
                dust_raw=float(air['dust_raw']),
                dust_Vo=float(air['dust_Vo']),
                dust_Voc=float(air['dust_Voc']),
                dust_dV=float(air['dust_dV']),
                dust_Vo_mV=float(air['dust_Vo_mV']),
                dustDensity=float(air['dustDensity']),
            )
    else:
            print("-------")
            print(air['eCO2'])
            print("---------")
            air = AirModel(
                city=air['city'],
                state=air['state'],
                country=air['country'],
                # zipcode=air['zipcode'],
                zipcode=zipcode,
                place=air['place'],
                details=air['details'],
                misc=air['misc'],
                tVOC=float(air['tVOC']),
                eCO2=float(air['eCO2']),
                # temp=float(air['temp']),
                temp=temp,
                pressure=float(air['pressure']),
                # altitude=float(air['altitude']),
                altitude=altitude,
                humidity=float(air['humidity']),
                mq2_raw=mq2_raw,
                mq2_ro=float(air['mq2_ro']),
                mq2_rs_by_ro=float(air['mq2_rs_by_ro']),
                mq2_lpg_ppm=float(air['mq2_lpg_ppm']),
                mq2_co_ppm=float(air['mq2_co_ppm']),
                mq2_smoke_ppm=float(air['mq2_smoke_ppm']),
                mq2_ref_ro=MQ2_Ref_Ro,
                mq2_ref_lpg_ppm=mq2_ref_lpg_ppm,
                mq2_ref_co_ppm=mq2_ref_co_ppm,
                mq2_ref_smoke_ppm=mq2_ref_smoke_ppm,
                mq4_raw=mq4_raw,
                mq4_ro=float(air['mq4_ro']),
                mq4_rs_by_ro=float(air['mq4_rs_by_ro']),
                # mq4_ng_ppm=float(air['mq4_ng_ppm']),
                mq4_ng_ppm=mq4_ng_ppm,
                mq4_ng_ppm2=float(air['mq4_ng_ppm2']),
                mq4_ref_ro=MQ4_Ref_Ro,
                mq4_ref_ng_ppm=mq4_ref_ng_ppm,
                mq6_raw=mq6_raw,
                mq6_ro=float(air['mq6_ro']),
                mq6_rs_by_ro=float(air['mq6_rs_by_ro']),
                mq6_lpg_ppm=float(air['mq6_lpg_ppm']),
                mq6_lpg_ppm2=float(air['mq6_lpg_ppm2']),
                mq6_ref_ro=MQ6_Ref_Ro,
                mq6_ref_lpg_ppm=mq6_ref_lpg_ppm,
                mq7_raw=mq7_raw,
                mq7_ro=float(air['mq7_ro']),
                mq7_rs_by_ro=float(air['mq7_rs_by_ro']),
                mq7_co_ppm=float(air['mq7_co_ppm']),
                mq7_h2_ppm=float(air['mq7_h2_ppm']),
                mq7_co_ppm2=float(air['mq7_co_ppm2']),
                mq7_ref_ro=MQ7_Ref_Ro,
                mq7_ref_co_ppm=mq7_ref_co_ppm,
                mq7_ref_h2_ppm=mq7_ref_h2_ppm,
                mq131_raw=mq131_raw,
                mq131_ro=float(air['mq131_ro']),
                mq131_rs_by_ro=float(air['mq131_rs_by_ro']),
                mq131_o3_ppm=float(air['mq131_o3_ppm']),
                mq131_o3_ppm2=float(air['mq131_o3_ppm2']),
                mq131_ref_ro=MQ131_Ref_Ro,
                mq131_ref_o3_ppm=mq131_ref_o3_ppm,
                # co2_raw=float(air['co2_raw']),
                # co2_ppm=float(air['co2_ppm']),
                co2_raw=co2_raw,
                co2_ppm=co2_ppm,
                dust_raw=float(air['dust_raw']),
                dust_Vo=float(air['dust_Vo']),
                dust_Voc=float(air['dust_Voc']),
                dust_dV=float(air['dust_dV']),
                dust_Vo_mV=float(air['dust_Vo_mV']),
                dustDensity=float(air['dustDensity']),
            )
    air = jsonable_encoder(air)       
    air = await collection.insert_one(air)
    created_air = await collection.find_one({"_id": air.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"log":"Air Pollution Record creation successful"})




