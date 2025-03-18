from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCharts import QChart, QChartView, QValueAxis, QStackedBarSeries
from PySide6.QtGraphs import QBarSet
from PySide6.QtGui import QPainter


APP_NAME = "Weather Fetcher"


class WeatherWidget(QtWidgets.QWidget):
    def __init__(self, cities, temperature, unit="°C", x=0):
        super().__init__()
        self.temperature = temperature
        self.unit = unit
        self.series = None
        self.chart = None
        self.cities = cities

        self.setWindowTitle(APP_NAME)
        self.resize(800, 600)

        self.title = QtWidgets.QLabel(APP_NAME)
        self.set_font_and_align_text(self.title, size=30)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.create_temperature_chart())
        self.x = x
        self.timer = None



    @staticmethod
    def set_font_and_align_text(item, font="Arial", size=20, align=QtCore.Qt.AlignmentFlag.AlignCenter):
        item.setFont(QtGui.QFont(font, size, QtGui.QFont.Weight.Bold))
        item.setAlignment(align)

    def show_temperature_for_city(self) -> None:
        for city in self.cities:
            temp_label = QtWidgets.QLabel(f"Temperature in {city}: {self.temperature[city]}{self.unit}")
            self.set_font_and_align_text(temp_label)
            self.layout.addWidget(temp_label)



    def create_temperature_chart(self):
        bar_set = QBarSet("Temperature")
        categories = []
        for city, temp in self.temperature.items():
            categories.append(city)
            bar_set.append(temp)

        # print(bar_set, type(bar_set))
        series = QStackedBarSeries()
        series.append(bar_set)  # to be fixed, not working for some reason

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Temperature records in Celcius")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # X-Axis (Cities)
        axis_x = QValueAxis()
        axis_x.setLabelsAngle(-45)
        axis_x.setRange(0, len(categories))
        chart.addAxis(axis_x, QtCore.Qt.AlignmentFlag.AlignBottom)

        # Y-Axis (Temperature)
        axis_y = QValueAxis()
        chart.addAxis(axis_x, QtCore.Qt.AlignmentFlag.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing, True)

        return chart_view
