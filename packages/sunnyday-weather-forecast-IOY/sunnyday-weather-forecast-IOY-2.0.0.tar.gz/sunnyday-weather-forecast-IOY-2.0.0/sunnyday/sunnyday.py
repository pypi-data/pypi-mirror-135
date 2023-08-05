import requests

api = "26631f0f41b95fb9f5ac0df9a8f43c92"


class Weather:
    """Creates a weather object getting an api key as input
    and either a city or lat and lon coordinates

    Package use example:

    # Create a weather object using a city name:
    # The api key below is not guaranteed to work
    # Get your own apikey from https://openweathermap.org
    # Wait for a couple of hours for the apikey to be activated

    >>> weather1 = Weather(apikey="26631f0f41b95fb9f5ac0df9a8f43c92", city="madrid")

    # using latitude and longitude coordinates
    >>> weather2 = Weather(apikey="26631f0f41b95fb9f5ac0df9a8f43c92", lat=41.1, lon=-4.1)

    # Get complete weather data for the next 12 hours
    >>> weather1.next_12h()

    # simplified data for the next 24 hours
    >>> weather1.next_12h_simplified()

    Sample URL to get sky condition icons:
    http://openweathermap.org/img/wn/10d@2x.png
    """

    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Provide either a city name or Lat and Lon arguments.")

        if self.data['cod'] != "200":
            raise ValueError(self.data['message'])

    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dict.
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, temperature, sky condition data and icons, every 3 hours
           for the next 12 hours as a list of tuples.
        """
        simple_data = []
        for i in self.data['list'][:4]:
            simple_data.append(
                (i['dt_txt'], i['main']['temp'], i['weather'][0]['description'], i['weather'][0]['icon']))
        return simple_data

