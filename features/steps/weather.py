from behave import *
from behave.api.async_step import async_run_until_complete
from app.utils import search_for_weather
from app.weather_fetcher import WeatherFetcher
import logging
import re

logger = logging.getLogger("ColorFormatter")


@given('the city "{city}" is provided to the Weather Fetcher')
def step_impl(context, city):
    context.fetcher = WeatherFetcher([city], False)
    fetched_city = context.fetcher.cities[0]
    logger.info(f"City fetched by Weather Fetcher:{fetched_city}, city provided by user:{city}")
    assert fetched_city == city

@when('the weather data is fetched for the "{city}" city')
@async_run_until_complete
async def step_impl(context, city):
    context.weather_data = await context.fetcher.get_weather()
    logger.info(f"Weather data fetched for the {city} city:{context.weather_data}")
    assert "weather" in search_for_weather(context.weather_data)
    assert city in context.weather_data.keys()


@then('the temperature for the city should be displayed')
@async_run_until_complete
async def step_impl(context):
    context.temp_data = await context.fetcher.get_temperature()
    logger.info(f"Temperature fetched for the city:{context.temp_data}")
    logger.info(f"Type of context.temp_data: {type(context.temp_data)}")
    assert context.temp_data is not None and re.search(r"^\d+\.\d+$", str(context.temp_data))
