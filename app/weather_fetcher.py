import requests
import logging
import utils

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()])

API_KEY = utils.decrypt_api_key()

class WeatherFetcher:

    def __init__(self, city: str):
        self._city = None
        self.set_city(city)

    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str):
        if not utils.validate_user_input_for_city_name(value):
            raise ValueError(f"Invalid city name: {value}")
        self._city = value


    def set_city(self, city: str):
        self.city = city

    def get_weather(self) -> dict:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            utils.save_weather_output_to_file(response, "output.json")
            if response.text:
                logger.info(f"Provided url {url} exists.")
                return response.json()
            else:
                logger.error(f"Provided url {url} does not exist or is corrupted.")
                return {"error": "Empty response body"}
        except requests.exceptions.RequestException as e:
            return {"error": "Request failed", "message": str(e)}

    def get_temperature(self):
        stats = self.get_weather()
        temp = stats["main"]["temp"]
        return logger.info(f"Current temperature in {self.city} is {temp:.1f} Celsius degree.")


init = WeatherFetcher(city="Wroclaw")
init.get_temperature()

# KOLEJNY KROK - DOROBIENIE ASYNCIO
# Provide an asynchronous feature,
# like fetching data for multiple cities simultaneously, using asyncio.