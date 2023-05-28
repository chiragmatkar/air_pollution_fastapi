from variables import * 
from datetime import date, datetime, timedelta
from apps.graph import timeseries_graphs
from app.models import Air, AirSchema
from variables import *
from functions.calculate_on_ref_Ro import *





# CSV HOURLY DATA HARI hari
def csv_hourly_data(zipcode, num_of_days=ONE_DAY):
    pollutants_vals = ["N/A"] * NUM_OF_POLLLUTANTS
    pollutants_units = [""] * NUM_OF_POLLLUTANTS
    bar_vals = [0] * NUM_OF_POLLLUTANTS
    bar_colors = ["GREEN"] * NUM_OF_POLLLUTANTS
    pollutants_states = ["N/A"] * NUM_OF_POLLLUTANTS
    weather_vals = ["N/A"] * 4
    weather_units = [""] * 4
    aqi_val = 0

    POLLUTANTS_DATA_AVAILABLE = True
    WEATHER_DATA_AVAILABLE = True

    past_time = datetime.now() - timedelta(days=num_of_days)

    airdata = Air.query.with_entities(
        Air.dustDensity,
        Air.tVOC,
        Air.co2_ppm,
        Air.mq131_o3_ppm,
        Air.mq7_co_ppm,
        Air.mq2_smoke_ppm,
        Air.mq6_lpg_ppm,
        Air.mq4_ng_ppm,
        Air.eCO2,
        Air.mq7_h2_ppm,
        Air.temp,
        Air.humidity,
        Air.pressure,
        Air.altitude,
    ).filter(Air.zipcode == zipcode, Air.timestamp >= past_time).all()

    print(airdata)
    print("^^^^^^^^^^^^^^^^^^")

    air_avgs = airdata[0]

    total_nones = air_avgs.count(None)
    if total_nones == 14:
        POLLUTANTS_DATA_AVAILABLE = False
        WEATHER_DATA_AVAILABLE = False
    else:
        pollut_nones = air_avgs[:10].count(None)
        weather_nones = air_avgs[10:].count(None)

        if pollut_nones == 10:
            POLLUTANTS_DATA_AVAILABLE = False
        if weather_nones == 4:
            WEATHER_DATA_AVAILABLE = False

    if WEATHER_DATA_AVAILABLE:
        # altitude adjustment
        val = air_avgs[13]
        if zipcode == '94720':
            if val < 150:
                val = 177.0
            elif val > 210:
                val = 177.0
        elif zipcode == '95014':
            if val < 180:
                val = 236.0
            elif val > 250:
                val = 236.0
        elif zipcode == '95064':
            if val < 650:
                val = 763.0
            elif val > 850:
                val = 763.0
        elif zipcode == '96150':
            if val < 5500:
                val = 6263.0
            elif val > 6350:
                val = 6263.0
        elif zipcode == '94305':
            if val < 135:
                val = 141.0
            elif val > 155:
                val = 141.0

        weather_vals = [air_avgs[10], air_avgs[11], air_avgs[12], val]
        weather_units = WEATHER_UNITS

    if POLLUTANTS_DATA_AVAILABLE:
        lpgval = air_avgs[6]
        while lpgval > 10:
            lpgval = lpgval / 10

        ng_val = air_avgs[7]

        co_val = air_avgs[4] / 10
        smoke_val = air_avgs[5] / 10

        # PM25, tVOC, CO2, O3, CO, Smoke, LPG, NG, eCO2, H2
        pollutants_vals = [air_avgs[0], air_avgs[1], air_avgs[2], air_avgs[3],
                           co_val, smoke_val, lpgval, ng_val,
                           air_avgs[8], air_avgs[9]]

        print(air_avgs)
        print("------- vals --------")

        # Replacing no2 with co2
        # Replacing so2 with tVOC
        ugm3_pm25 = air_avgs[0]
        ugm3_tvoc = calculate_ugm3(60.9516, air_avgs[1])
        ugm3_co2 = calculate_ugm3(44.01, air_avgs[2])
        ugm3_o3 = calculate_ugm3(48.00, air_avgs[3])
        ugm3_co = calculate_ugm3(28.01, co_val)
        ugm3_pm10 = smoke_val

        final_aqi = (ugm3_co2 * 0.252687954 / 100) + (ugm3_tvoc * 0.400181718 / 10) + (ugm3_o3 * 0.429166667) + (
                ugm3_co * 0.00537414966) + (ugm3_pm25 * 1.248920438) + (ugm3_pm10 * 0.740816327 / 100.0)

        ######aqi_val = air_avgs[0]*1.248920438 + air_avgs[3]*0.429166667 + air_avgs[4]*5.37414966
        # aqi_val = air_avgs[0]*1.248920438 + air_avgs[1]*0.740816327 + air_avgs[2]*0.400181718 + air_avgs[3]*0.429166667
        aqi_val = final_aqi
        aqi_val = round(aqi_val)
        pollutants_units = POLLUTANTS_UNITS
        pollutants_states = []
        bar_colors = []
        bar_vals = []

        # PM2.5
        state, color = get_PM25_state_barColor(pollutants_vals[0])
        pollutants_states.append(state)
        bar_colors.append(color)
        val = get_barValue(air_avgs[0], PM25_max)
        bar_vals.append(val)

        # TVOC
        state, color = get_VOC_state_barColor(air_avgs[1])
        pollutants_states.append(state)
        bar_colors.append(color)
        val = get_barValue(air_avgs[1], tVOC_max)
        bar_vals.append(val)

        # CO2
        state, color = get_CO2_state_barColor(air_avgs[2])
        pollutants_states.append(state)
        bar_colors.append(color)
        val = get_barValue(air_avgs[2], CO2_max)
        bar_vals.append(val)

        # O3
        state, color = get_O3_state_barColor(air_avgs[3])
        pollutants_states.append(state)
        bar_colors.append(color)
        val = get_barValue(air_avgs[3], O3_max)
        bar_vals.append(val)

        # CO
        # state, color = get_CO_state_barColor(air_avgs[4])
        state, color = get_CO_state_barColor(co_val)
        pollutants_states.append(state)
        bar_colors.append(color)
        # val =  get_barValue(air_avgs[4], CO_max)
        val = get_barValue(co_val, CO_max)
        bar_vals.append(val)

        # Smoke
        # state, color = get_Smoke_state_barColor(air_avgs[5])
        state, color = get_Smoke_state_barColor(smoke_val)
        pollutants_states.append(state)
        bar_colors.append(color)
        # val =  get_barValue(air_avgs[5], Smoke_max)
        val = get_barValue(smoke_val, Smoke_max)
        bar_vals.append(val)

        # LPG
        state, color = get_LPG_state_barColor(air_avgs[6])
        pollutants_states.append(state)
        bar_colors.append(color)
        val = get_barValue(air_avgs[6], LPG_max)
        bar_vals.append(val)

        # NG
        # state, color = get_NG_state_barColor(air_avgs[7])
        state, color = get_NG_state_barColor(ng_val)
        pollutants_states.append(state)
        bar_colors.append(color)

        # GAYATRI
        # air_avgs[7] = 10
        val = get_barValue(ng_val, NG_max)
        bar_vals.append(val)

        # eCO2
        state, color = get_eCO2_state_barColor(air_avgs[8])
        pollutants_states.append(state)
        bar_colors.append(color)
        val = get_barValue(air_avgs[8], CO2_max)
        bar_vals.append(val)

        # H2
        state, color = get_H2_state_barColor(air_avgs[9])
        pollutants_states.append(state)
        bar_colors.append(color)
        # PUT H2 MAX
        val = get_barValue(air_avgs[9], CO_max)
        bar_vals.append(val)

    geo = Air.query.with_entities(
        Air.city,
        Air.state,
        Air.country,
        Air.place
    ).filter(Air.zipcode == zipcode).first()

    if geo:
        location_data = {
            "zipCode": zipcode,
            "city": geo[0],
            "state": geo[1],
            "country": geo[2],
            "place": geo[3]
        }
    else:
        location_data = {
            "zipCode": zipcode,
            "city": "N/A",
            "state": "N/A",
            "country": "N/A",
            "place": "N/A"
        }
    pollutants_data = []
    for i in range(10):
        d = {
            "name": POLLUTANTS_NAMES[i],
            "abbr": POLLUTANTS_ABBR[i],
            "value": pollutants_vals[i],
            "units": POLLUTANTS_UNITS[i],
            "state": pollutants_states[i],
            "barProgress": bar_vals[i],
            "barColor": bar_colors[i],
            "tipsTitle": POLLUTANTS_TIPS_TITLES[i],
            "tipsContent": POLLUTANTS_TIPS_CONTENTS[i],
            "order": POLLUTANTS_ORDER[i]
        }
        pollutants_data.append(d)

    weather_data = [
        {
            "name": NAME_TEMP,
            "abbr": ABBR_TEMP,
            "value": weather_vals[0],
            "unit": weather_units[0],
            "order": ORDER_TEMP
        },
        {
            "name": NAME_HUMIDITY,
            "abbr": ABBR_HUMIDITY,
            "value": weather_vals[1],
            "unit": weather_units[1],
            "order": ORDER_HUMIDITY
        },
        {
            "name": NAME_PRESSURE,
            "abbr": ABBR_PRESSURE,
            "value": weather_vals[2],
            "unit": weather_units[2],
            "order": ORDER_PRESSURE
        },
        {
            "name": NAME_ALTITUDE,
            "abbr": ABBR_ALTITUDE,
            "value": weather_vals[3],
            "unit": weather_units[3],
            "order": ORDER_ALTITUDE
        },
    ]

    print(pollutants_data)

    data = {
        "pollutantDetails": pollutants_data,
        "weatherDetails": weather_data,
        "locationDetails": location_data,
        "aqi": aqi_val
    }
    print("DATA DATA DATA")
    print(data)
    print("DATA DATA DATA")
    return data
