import json
import plotly.express as px
from datetime import datetime


DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYBMOL}"

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year Hour Minutes
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime("%A %d %B %Y %H:%M")


def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celcius

    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celcius.
    """
    temp_in_celsius = (temp_in_farenheit -32) * 5/9
    temp_in_celsius = round(temp_in_celsius,1) #limits the number to only one decimal place
    return temp_in_celsius
    

def graph_weather(forecast_file):

    #Daily forecast contains data per day
    #Daily forecast is a list of dictionaries. 
    #Dictionaries inside daily forecast are: 
    #Moon, Temperature - inside dict for min and another for max,
    #realfeeltemp/min and max, degree summary/heating, cooling, airandpollen,
    
    #Step 1: 
    #Need to be able to read each Date dict, and within than read temp for max and min

    """Converts raw weather data into meaningful text, generates the relevant graphs and output txt file

    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """
    
    with open(forecast_file) as json_file: 
        json_data = json.load(json_file) 
    
    date_list = []
    temp_list = []
    rftemp_list = []  
    wtxt_list = []  
    wqty_list = []
    wtxt2_list = []
    w_dict = {}
    precip_list = []
    counter = 0
    precip_hours = 0
    daylight_list = []
    daylight_hours = 0
    UVindex_list = []

    x1_list = []
    counter_aux = 0

    #Extracting data from json file
    for parcel in json_data:
        for key, value in parcel.items():
            if key == "LocalObservationDateTime":
                date_value = convert_date(value)
                date_list.append(date_value)
            
            if key == "Temperature":
                for key1, value1 in value.items():
                    if key1 == "Metric":
                        for key2, value2 in value1.items():
                            if key2 == "Value":
                                temp = int(value2)
                                temp_list.append(temp) #this is in Celsius already

            if key == "RealFeelTemperature":
                for key1, value1 in value.items():
                    if key1 == "Metric":
                        for key2, value2 in value1.items():
                            if key2 == "Value":
                                rftemp = int(value2)
                                rftemp_list.append(rftemp)

            if key == "WeatherText":
                wtxt = value
                wtxt_list.append(wtxt)
            
            if key == "Precip1hr":
                for key1, value1 in value.items():
                    if key1 == "Metric":
                        for key2, value2 in value1.items():
                            if key2 == "Value":
                                precip = float(value2)
                                if precip > 0:
                                    precip_hours = precip_hours + 1 #number of hours that precip was recorded
                                precip_list.append(precip) #values in mm

            if key == "PrecipitationSummary":
                for key1, value1 in value.items():
                    if key1 == "Past24Hours":
                        for key2, value2 in value1.items():
                            if key2 == "Metric":
                                for key3, value3 in value2.items():
                                    if key3 == "Value":
                                        if counter == 0:
                                            precip_24hrs = value3 #this will record the 24hr value of the first date/hour which is the latest one
                                            counter = counter + 1
                
            #Calculate Daylight hours
            if key == "IsDayTime":
                daylight = value
                daylight_list.append(daylight)
                
                if daylight:
                    daylight_hours = daylight_hours + 1

            #Find UV index
            if key == "UVIndex":
                UVindex = int(value)
                UVindex_list.append(UVindex)
                

    # print(date_list)
    # print(f"Temp: {temp_list}")
    # print(f"Real Feel Temp: {rftemp_list}")
    print(precip_list)

    #Determine the number of times the same weather text category appears in the weather text list by creating a dictionary
    for parcel in wtxt_list:
        if parcel in w_dict:
            w_dict[parcel] = w_dict[parcel] + 1
        else:
            w_dict[parcel] = 1

    for key in w_dict:
        wtxt2_list.append(key)
        wqty_list.append(w_dict[key])

#    # print(f"Dict = {w_dict} {len(w_dict)}")
#     print(f"Weather: {wtxt2_list}")
#     print(f"Weather 2: {wqty_list}")

    #Determine when the min and max temp occurred
    # MIN TEMP
    min_temp = min(temp_list) #Calculates the min value in the temp list
    min_temp_formatted = format_temperature(str(min_temp))#formatting temp
   
    #Also need the date when overall min happens, so will use index function to find the position of overall min temp on the list
    min_pos = temp_list.index(min_temp) 
    #Therefore the date we are looking for happens in date_list in position min_pos
    date_min_temp = date_list[min_pos]

    #MAX TEMP
    max_temp = max(temp_list) #Calculates the max value in the temp list
    max_temp_formatted = format_temperature(str(max_temp)) #formatting temp

     #Also need the date when  max happens, so will use index function to find the position of max temp on the list
    max_pos = temp_list.index(max_temp)
    #Therefore the date we are looking for happens in date_list in position max_pos
    date_max_temp = date_list[max_pos]

    #MAX UV INDEX
    max_UV = max(UVindex_list)
    max_UV_pos = UVindex_list.index(max_UV)
    date_max_UV = date_list[max_UV_pos]

    #Preparing text to be written into text file
    a0 = f"MIN temperature recorded was: {min_temp_formatted} and it occurred on {date_min_temp} \n"
    a1 = f"MAX temperature recorded was: {max_temp_formatted} and it occurred on {date_max_temp} \n"    
    a2 = f"Amount of precipitation that fell in the last 24 hours (24hrs from {date_list[0]}) was {precip_24hrs}mm \n"
    a3 = f"Precipitation has been recorded for {precip_hours}hrs \n"
    a4 = f"Daylight has been recorded for {daylight_hours}hrs \n"
    a5 = f"MAX UV index recorded was: {max_UV} and it occurred on {date_max_UV} \n"
    num_hours = len(date_list)

    #GRAPH1 
    #Plotting two box plots containing temp and real feel temp

    #Creating the X labels for the box plot graph
    while counter_aux < num_hours/2:
        x1_list.append("Temperature")
        counter_aux = counter_aux + 1
    
    counter_aux = 0
    while counter_aux < num_hours/2:
        x1_list.append("Temperature Real Feel")
        counter_aux = counter_aux + 1

    # print(f"X1: {x1_list}")    

    fig = px.box(
        x=x1_list, 
        y=[temp_list,rftemp_list], 
        points="all", 
        title=f"Temp and Real Feel Temp in Perth over {num_hours} hours"
        )


    fig.update_layout(
        xaxis_title=f"Date Range from {date_list[len(date_list)-1]} to {date_list[0]}",
        yaxis_title="Temperature (°C)",
        )

    fig.write_html("Graph1.html") 
    # print(fig)

    #GRAPH 2 - Bar Chart

    fig = px.bar(x=wtxt2_list, y=wqty_list, barmode="group", title="Weather text categories")
    fig.update_layout(
        xaxis_title="Weather Text Category",
        yaxis_title="Number of times category appears in data file",
        )

    fig.write_html("Graph2_bar.html")
    # print(fig)

    with open("part3_output.txt", "w") as txt_file: #in this case specifying to open the file for writing by passing the 'w' 
        txt_file.write(f"Data file: {forecast_file} \n \n")
        txt_file.write(a0)
        txt_file.write(a1)
        txt_file.write(a2)
        txt_file.write(a3)
        txt_file.write(a4)
        txt_file.write(a5)

if __name__ == "__main__":
   graph_weather("data/historical_6hours.json")
