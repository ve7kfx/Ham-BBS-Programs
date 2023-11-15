import requests

def get_weather(city):
    formatted_city = city.replace(' ', '_')  # Replaces spaces with underscores
    params = {
        'format': ("+Location:%l+\n+Condition:%x\n+Temperature:%t\n+Feels:%f\n"
                   "+Humidity:+%h\n+Pressure(hPa):+%P\n+Percipitation(mm/3+hours):+%p\n"
                   "+Wind:+%w\n+UV+index:+%u\n+Sunrise:+%S\n+Sunset:+%s\n"
                   "+Current+Time:+%T\n+Timezone:+%Z\n")
    }
    url = f'http://wttr.in/{formatted_city}'
    response = requests.get(url, params=params)
    return response.text

def main():
    print("Weather Lookup")
    print("----------------")
    city = input("Enter the city you'd like to look up: ")
    print("\nFetching weather data...\n")

    weather_info = get_weather(city)
    print(weather_info)

if __name__ == '__main__':
    main()
