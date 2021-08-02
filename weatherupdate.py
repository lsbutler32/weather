import requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="weatherupdate.py")
API = 'ENTER_YOUR_API_KEY_HERE' # API key from openweathermap

states = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
          "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
          "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
          "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
          "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
          "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
          "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
          "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
          "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin",
          "WY": "Wyoming"}

new_city = 'XXX'  # assigning value to new_city for single city inputs to keep proper checks


def coordinates(latitude, longitude):
    """
    Uses the latitude and longitude to find the state at which the city provided is from and checks if it matches
    the provided state
    :param latitude: Str of digits for a city's latitude
    :param longitude: Str of digits for a city's longitude
    :return: Str of a city's state
    """
    location = geolocator.reverse(latitude + ", " + longitude)
    data = location.raw
    data = data['address']
    state_code = data['state']
    return state_code


def current_weather(city_name, API):
    """
    Provides the weather for any city in world within the openweather API using city,country or city,state or zip or
    just city
    :param city_name: Str in format of just city or city,state or city,country code or zip code
    :param API: Str of API key
    :return: a Str of parsed data for the city provided
    """
    global new_city
    try:
        if city_name.isnumeric():  # if input is zip
            url = f'http://api.openweathermap.org/data/2.5/weather?zip={city_name},&appid={API}'
        elif ',' in city_name:  # if input has a city,state or city,country
            new_city = city_name.split(',')
            new_city_name = new_city[0].replace(' ', '%20')  # so the url correctly handles spaces in cities
            if len(new_city[1]) > 2:  # if the state/country code is invalid
                return "Not valid state code/country code"
            url = f'https://api.openweathermap.org/data/2.5/weather?q={new_city_name},{new_city[1]},us&appid={API}'
        elif ',' not in city_name:  # if searched by only city and not state or country code, works for big cities
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}'
        response = requests.get(url).json()  # getting the proper json data based on the input of the city_name
        city_latitude = str(response['coord']['lat'])
        city_longitude = str(response['coord']['lon'])
        if (new_city[1].upper() in states) and (
                response['sys']['country'] != 'US'):  # to catch foreign cities with US state codes
            return "Not valid city"
        elif (new_city[1].upper() not in states) and (
                new_city[1].upper() != response['sys']['country'] and new_city != 'XXX'):
            # to catch US cities with foreign country codes
            return 'Not a valid city'
        elif states[new_city[1].upper()] != coordinates(city_latitude,
                                                        city_longitude):
            # Check to see if city is located in provided state
            return 'City is not located in that state'
        current_temp = response['main']['temp']
        max_temp = response['main']['temp_max']
        min_temp = response['main']['temp_min']
        feels_like_temp = response['main']['feels_like']
        curr_temp_fheit = round((current_temp * 1.8) - 459.67)  # converting to imperial
        max_temp_fheit = round((max_temp * 1.8) - 459.67)
        min_temp_fheit = round((min_temp * 1.8) - 459.67)
        feels_like_temp_fheit = round((feels_like_temp * 1.8) - 459.67)
        description = response['weather'][0]['description']
        wind = round(response['wind']['speed'] * 2.23694)

        format_weather = ("Current weather for " + str(city_name) + ", " + response['sys']['country'] +
                          "\nCurrent temp: " + str(curr_temp_fheit) + '\nMax Temp: ' + str(
                    max_temp_fheit) + '\nMin Temp: ' + str(
                    min_temp_fheit) + '\nFeels like: ' + str(
                    feels_like_temp_fheit) + '\nOutlook: ' + description + '\nWind: ' + str(
                    wind) + ' mph')
        # print weather in cleaner format
        return format_weather

    except KeyError:  # If a city that doesn't exist is entered
        return 'Not valid city'
