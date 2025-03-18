from weather_fetcher import WeatherFetcher
from gui import WeatherWidget
from PySide6.QtWidgets import QApplication
import sys
import asyncio

DEFAULT_QR_CODE_CREATION = True

class App:
    def __init__(self, cities):
        self.app = QApplication(sys.argv)
        self.cities = cities
        # self.weather_widget = WeatherWidget(cities, temperature=None)
        self.weather_widget = None
        self.weather_fetcher = WeatherFetcher(cities = cities, create_qr_codes=DEFAULT_QR_CODE_CREATION)

    def run_gui(self):
        self.weather_widget.show()
        sys.exit((self.app.exec()))

if __name__ == "__main__":
    application = App(cities=["Wroclaw", "London", "Amsterdam"])
    temperature = asyncio.run(application.weather_fetcher.get_temperature())
    application.weather_widget = WeatherWidget(application.cities, temperature)
    application.weather_widget.temperature = temperature
    application.weather_widget.show_temperature_for_city()
    application.weather_widget.create_temperature_chart()
    application.run_gui()
