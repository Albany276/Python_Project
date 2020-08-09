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
        A date formatted like: Weekday Date Month Year
    """
    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime("%A %d %B %Y")


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

    """Converts raw weather data into meaningful text.

    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """
    
    with open(forecast_file) as json_file: 
        json_data = json.load(json_file) 
    
    count_min_temp = 0
    count_max_temp = 0
    min_temp_C_total = 0
    max_temp_C_total = 0

    min_temp_list = []
    max_temp_list = []
    date_list = []

    rft_min_list = []
    rfts_min_list = []

    #Json_data is a dictionary with 2 keys, Headline and DailyForecasts
    for key, value in json_data.items():
        # print(key, value)

        if key == "DailyForecasts":
            #DailyForecast is a list, that is why the for below is written that way
            for parcel in value:
                #For json file - forecasts 5days
                #Parcel0 is date 19/06
                #Parcel1 is date 20/06
                #Parcel2 is date 21/06
                #Parcel3 is date 22/06
                #Parcel4 is date 23/06

                #Every parcel is a dictionary with keys1 being date, epochdate, sun, moon, temperature, etc.
                for key1, value1 in parcel.items():

                    #Grabbing date value from Dict
                    if key1 == "Date":
                        date_value = value1
                        #Formatting date to human readable
                        date_value_formatted = convert_date(date_value)
                        date_list.append(date_value_formatted) #holding all values in a list
                        # print(f"{date_value_formatted}")

                    #Temperature is also a dictionary, where key2 is minimum and maximum
                    if key1 == "Temperature":
                        for key2, value2 in value1.items():
                            #Maximum and Minimum are also dictionaries, with keys value, unit, unittype
                            if key2 == "Minimum":
                                # print("Min")
                                for key3, value3 in value2.items(): 
                                    #we are after key3=value which contains the temp value
                                    if key3 == "Value":
                                        
                                        min_temp = int(value3) #this temp is in Farenheit
                                        min_temp_C = convert_f_to_c(min_temp) #converting to Celsius
                                        min_temp_list.append(min_temp_C) #holding all values in a list - creating list with temp in int rather than str so we can perform min and max functions on the list without issues.

                                        #Preparing for using the mean function
                                        # count_min_temp = count_min_temp + 1 #This will hold the number of items
                                        # min_temp_C_total = min_temp_C + min_temp_C_total #This will hold the total

                            if key2 == "Maximum":   
                                # print("Max") 
                                for key4, value4 in value2.items():
                                    #we are after key4=value which contains the temp value
                                    if key4 == "Value":
                                        max_temp = int(value4) #this temp is in Farenheit
                                        max_temp_C = convert_f_to_c(max_temp) #converting to Celsius
                                        max_temp_list.append(max_temp_C) #holding all values in a list - creating list with temp in int rather than str so we can perform min and max functions on the list without issues.

                                        #Preparing for using the mean function
                                        # count_max_temp = count_max_temp + 1 #This will hold the number of items
                                        # max_temp_C_total = max_temp_C + max_temp_C_total #This will hold the total

                    #RealFeelTemperature is a dictionary whitin the parcel dictionary                
                    if key1 == "RealFeelTemperature":
                        # Need to iterate within RealFeelTemp dict to get the Minimum
                        #STOPPED HERE
                        for key2, value2 in value1.items():
                            if key2 == "Minimum":
                                
                                for key3, value3 in value2.items(): 
                                    #we are after key3=value which contains the temp value
                                    if key3 == "Value":
                                        rft_min_F = int(value3) #temp in Farenheit
                                        rft_min_C = convert_f_to_c(rft_min_F) #converting to Celsius
                                        rft_min_list.append(rft_min_C) #holding all values in a list

                    #RealFeelTemperatureShade is a dictionary whitin the parcel dictionary                
                    if key1 == "RealFeelTemperatureShade":
                        # Need to iterate within RealFeelTempShade dict to get the Minimum
                        for key2, value2 in value1.items():
                            if key2 == "Minimum":
                                for key3, value3 in value2.items(): 
                                    #we are after key3=value which contains the temp value
                                    if key3 == "Value":
                                        rfts_min_F = int(value3) #temp in Farenheit
                                        rfts_min_C = convert_f_to_c(rfts_min_F) #converting to Celsius
                                        rfts_min_list.append(rfts_min_C) #holding all values in a list
                                       

   
    print(f"Temp Min: {min_temp_list}")
    print(f"Temp Max: {max_temp_list}")
    # print(f"RFT Min: {rft_min_list}")
    # print(f"RFTS Min: {rfts_min_list}")
    
    num_days = len(date_list)

    #GRAPH1:
    #Plotting Min and Max temperatures in the same chart
    fig = px.line(  
        x=date_list,
        y=[min_temp_list, max_temp_list],
        title=f"Min and Max temperatures in Perth over {num_days} days"
        )
    
    #Setting the colours and the names that will be used on the legend
    fig.data[0].name = "Min temperatures"
    fig.data[0].line.color = "#9400D3"
    fig.data[1].name = "Max temperatures"
    fig.data[1].line.color = "#FFA500"
    
    #Updating the titles of the axis and legend
    fig.update_layout(
        xaxis_title="Dates",
        yaxis_title="Temperature (°C)",
        legend_title_text="Legend:")


    fig.write_html("Graph1.html") 
    # print(fig)

    #GRAPH2:
    #Plotting Min, Min Real Feel and Min Real Feel Shade in the same chart
    fig = px.line(  
        x=date_list,
        y=[min_temp_list, rft_min_list, rfts_min_list],
        title=f"Min, Min Real Feel and Min Real Feel Shade temperatures in Perth over {num_days} days"
        )
    
    #Setting the colours and the names that will be used on the legend
    fig.data[0].name = "Min temperatures"
    fig.data[0].line.color = "#9400D3"
    fig.data[1].name = "Min Real Feel temperatures"
    fig.data[1].line.color = "#FFA500"
    fig.data[1].line.dash = "dot"
    fig.data[2].name = "Min Real Feel Shade temperatures"
    fig.data[2].line.color = "#C0C0C0"
    fig.data[2].line.dash = "dash"
    #fig.data[2].mode = "markers"
    
    
    #Updating the titles of the axis and legend
    fig.update_layout(
        xaxis_title="Dates",
        yaxis_title="Temperature (°C)",
        legend_title_text="Legend:")


    fig.write_html("Graph2.html") 
    # print(fig)


if __name__ == "__main__":
   graph_weather("data/forecast_5days_b.json")



