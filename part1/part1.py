import json
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
    


def calculate_mean(total, num_items):
    """Calculates the mean.
    
    Args:
        total: integer representing the sum of the numbers.
        num_items: integer representing the number of items counted.
    Returns:
        An integer representing the mean of the numbers.
    """
    mean1 = total / num_items
    mean1 = round(mean1, 1) #limiting to 1 decimal place
    return mean1


def process_weather(forecast_file):

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
    Day_phrase = []
    Day_rain = []
    Night_phrase =[]
    Night_rain = []
    b_total = ""


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
                                        count_min_temp = count_min_temp + 1 #This will hold the number of items
                                        min_temp_C_total = min_temp_C + min_temp_C_total #This will hold the total

                            if key2 == "Maximum":   
                                # print("Max") 
                                for key4, value4 in value2.items():
                                    #we are after key4=value which contains the temp value
                                    if key4 == "Value":
                                        max_temp = int(value4) #this temp is in Farenheit
                                        max_temp_C = convert_f_to_c(max_temp) #converting to Celsius
                                        max_temp_list.append(max_temp_C) #holding all values in a list - creating list with temp in int rather than str so we can perform min and max functions on the list without issues.

                                        #Preparing for using the mean function
                                        count_max_temp = count_max_temp + 1 #This will hold the number of items
                                        max_temp_C_total = max_temp_C + max_temp_C_total #This will hold the total

                    #Day is a dictionary whitin the parcel dictionary                
                    if key1 == "Day":
                        # Need to iterate within Day dict to get to LongPhrase and RainProbability
                        for key2, value2 in value1.items():
                            if key2 == "LongPhrase":
                                daytime_phrase = value2
                                Day_phrase.append(daytime_phrase) #holding all values in a list
                                # print(f"Daytime: {daytime_phrase}")

                            if key2 == "RainProbability":
                                rain_prob = value2
                                Day_rain.append(rain_prob) #holding all values in a list
                                # print(f"Rain prob is {rain_prob}%")

                     #Night is a dictionary whitin the parcel dictionary                
                    if key1 == "Night":
                         # Need to iterate within Day dict to get to LongPhrase and RainProbability
                         for key2, value2 in value1.items():
                            if key2 == "LongPhrase":
                                nighttime_phrase = value2
                                Night_phrase.append(nighttime_phrase) #holding all values in a list
                                #print(f"Nighttime: {nighttime_phrase}")

                            if key2 == "RainProbability":
                                n_rain_prob = value2
                                Night_rain.append(n_rain_prob) #holding all values in a list
                                # print(f"Night rain prob is {n_rain_prob}%")

    #Preparing for heading to be printed with min/max and average(mean) temps
    
    #OVERALL MIN TEMP
    overall_min_temp = min(min_temp_list) #Calculates the min value in the min_temp list
    overall_min_temp_formatted = format_temperature(str(overall_min_temp))#formatting temp
    # print(f"TYPE OF MIN value: {type(overall_min_temp_formatted)}")
    
    #Also need the date when overall min happens, so will use index function to find the position of overall min temp on the list
    min_pos = min_temp_list.index(overall_min_temp) 
    #Therefore the date we are looking for happens in date_list in position min_pos
    date_overall_min_temp = date_list[min_pos]

    #OVERALL MAX TEMP
    overall_max_temp = max(max_temp_list) #Calculates the max value in the max_temp list
    overall_max_temp_formatted = format_temperature(str(overall_max_temp)) #formatting temp

     #Also need the date when overall max happens, so will use index function to find the position of overall max temp on the list
    max_pos = max_temp_list.index(overall_max_temp)
    #Therefore the date we are looking for happens in date_list in position max_pos
    date_overall_max_temp = date_list[max_pos]

    #AVERAGE MIN TEMP
    #Calculating mean min temp - the arguments are already in celsius, so the mean would also be in celsius
    min_temp_mean = calculate_mean(min_temp_C_total, count_min_temp)
    #Formatting mean min temp
    min_temp_mean_string = str(min_temp_mean)
    min_temp_mean_formatted = format_temperature(min_temp_mean_string)
    # print(f"TYPE OF MIN value: {type(min_temp_mean_formatted)}")

    #AVERAGE MAX TEMP
    max_temp_mean = calculate_mean(max_temp_C_total, count_max_temp)
    #Formatting mean max temp
    max_temp_mean_string = str(max_temp_mean)
    max_temp_mean_formatted = format_temperature(max_temp_mean_string)

    
    
    num_days = len(date_list)
    #a = f"{num_days} Day Overview\n    The lowest temperature will be {overall_min_temp_formatted}, and will occur on {date_overall_min_temp}.\n    The highest temperature will be {overall_max_temp_formatted}, and will occur on {date_overall_max_temp}.\n    The average low this week is {min_temp_mean_formatted}.\n    The average high this week is {max_temp_mean_formatted}."
   
    #The function needs to return a single string in the right format. Preparing first paragraph:
    a0 = f"{num_days} Day Overview"
    a1 = f"\n    The lowest temperature will be {overall_min_temp_formatted}, and will occur on {date_overall_min_temp}."
    a2 = f"\n    The highest temperature will be {overall_max_temp_formatted}, and will occur on {date_overall_max_temp}."
    a3 = f"\n    The average low this week is {min_temp_mean_formatted}."
    a4 = f"\n    The average high this week is {max_temp_mean_formatted}."
    a_total = a0 + a1 + a2 + a3 + a4

    counter = len(date_list) - 1

    while counter >= 0: #this works because all lists are the same lenght - starting from len of list to zero, so the resulting string gets saved on the right order

        #Formatting min temp
        min_temp_C_string = str(min_temp_list[counter]) #converting to string in order to use format temp function
        min_temp_C_formatted = format_temperature(min_temp_C_string) #adding Celsius degrees to the temp format

        #Formatting max temp
        max_temp_C_string = str(max_temp_list[counter]) #converting to string to be able to use the format temp function
        max_temp_C_formatted = format_temperature(max_temp_C_string)
  
        #Preparing the second part of the output - it all needs to be part of one string
        b0 = f"\n-------- {date_list[counter]} --------"
        b1 = f"\nMinimum Temperature: {min_temp_C_formatted}"
        b2 = f"\nMaximum Temperature: {max_temp_C_formatted}"
        b3 = f"\nDaytime: {Day_phrase[counter]}"
        b4 = f"\n    Chance of rain:  {Day_rain[counter]}%"
        b5 = f"\nNighttime: {Night_phrase[counter]}"
        b6 = f"\n    Chance of rain:  {Night_rain[counter]}%"

        b_total =  "\n" + b0 + b1 + b2 + b3 + b4 + b5 + b6 + b_total
        counter = counter -1

    resulting_string = a_total + b_total +"\n" + "\n"
    return resulting_string


if __name__ == "__main__":
    print(process_weather("data/forecast_5days_b.json"))






