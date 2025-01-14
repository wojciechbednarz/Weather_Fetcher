from typing import Any
import storage
import logging
import utils
import asyncio
import aiohttp

class ColorFormatter(logging.Formatter):
    """
        Custom formatter to colorize error messages.
    """

    RED = "\033[31m"   # ANSI code for red
    YELLOW = "\033[33m"  # ANSI code for yellow
    WHITE = "\033[32m" # ANSI code for green
    RESET = "\033[0m"  # ANSI code to reset color

    def format(self, record):
        original_msg = super().format(record)

        if record.levelno == logging.ERROR or record.levelno == logging.WARNING:
            colored_msg = f"{self.RED}{original_msg}{self.RESET}"
        elif record.levelno == logging.WARNING:
            colored_msg = f"{self.YELLOW}{original_msg}{self.RESET}"
        else:
            colored_msg = f"{self.WHITE}{original_msg}{self.RESET}"
        return colored_msg

logger = logging.getLogger("ColorFormatter")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = ColorFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

API_KEY = utils.decrypt_api_key()

class WeatherFetcher:

    def __init__(self, cities: list, create_qr_codes: bool):
        self._cities = []
        self.set_cities(cities)
        self.create_qr_codes = create_qr_codes

    @property
    def cities(self) -> list[Any]:
        return self._cities

    @cities.setter
    def cities(self, cities: str):
        for city in self._cities:
            if not utils.validate_user_input_for_city_name(city):
                raise ValueError(f"Invalid city name: {city}")
        self._cities = cities

    def set_cities(self, cities: list):
        self.cities = cities

    async def get_weather(self) -> dict:
        results = {}
        async with aiohttp.ClientSession() as session:
            for city in self._cities:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
                await storage.save_city_weather_link_as_qr_code(url, city)
                try:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.json()  # Await JSON parsing
                        await storage.save_weather_output_to_file(data, "output.json", city)  # Save the data
                        logger.info(f"Fetched weather for {city}: {url}")
                        results[city] = data
                except aiohttp.ClientError as e:
                    logger.error(f"Request failed for {city}: {e}")
                    results[city] = {"error": "Request failed", "message": str(e)}
                except Exception as e:
                    logger.error(f"An error occurred while fetching data for {city}: {e}")
                    results[city] = {"error": "Unknown error", "message": str(e)}
        return results

    async def get_temperature(self):
        weather_data = await self.get_weather()
        for city, data in weather_data.items():
            if "main" in data:
                temp = data["main"]["temp"]
                logger.info(f"Current temperature in {city} is {temp:.1f} Celsius degree.")
            else:
                logger.error(f"Could not fetch temperature for {city}: {data.get('error')}")

async def main():
    cities = ["Wroclaw", "London"]
    fetcher = WeatherFetcher(cities, True)
    await fetcher.get_temperature()

if __name__ == '__main__':
    asyncio.run(main())
