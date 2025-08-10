import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Search", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()


        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)


        self.setLayout(vbox)


        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)


        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")


        self.setStyleSheet("""
                           QLabel, QPushButton {
                           font-family: Calibri;
                           }
                           QLabel#city_label {
                           font-size: 40px;
                           font-style: italic;
                           }
                           QLineEdit#city_input {
                           font-size: 40px;
                           }
                           QPushButton#get_weather_button {
                           font-size: 30px;
                           font-weight: bold;
                           }
                           QLabel#temperature_label {
                           font-size: 75px;
                           }
                           QLabel#emoji_label {
                           font-size: 100px;
                           font-family: Segoe UI emoji;
                           }
                           QLabel#description_label{
                           font-size: 50px;
                           }
                           """)
       
        self.get_weather_button.clicked.connect(self.get_weather)
   
    def get_weather(self):


        api_key = #get your own API key at 'https://www.weatherapi.com/'
        city = self.city_input.text()
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"


        global response
        response = requests.get(url)
        data = response.json()


        if response.status_code == 200:
            self.display_weather(data)
        else:
            self.display_error()


    def display_error(self):
        code = response.status_code
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(f"{code} Error.\nTry Again.")
        self.emoji_label.setText("❌")
   
    def display_weather(self, data):
        temp_c = data['current']['temp_c']
        self.temperature_label.setText(f"{temp_c}°C")
        self.description_label.setText(f"{data['current']['condition']['text']}")
        icon_url = data['current']['condition']['icon']
        self.set_weather_icon(icon_url)
   
    def set_weather_icon(self, icon_url):
        # WeatherAPI icon URLs start with '//', so prepend 'https:'
        if icon_url.startswith('//'):
            icon_url = 'https:' + icon_url
        response = requests.get(icon_url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            # Scale the pixmap to make the icon bigger and keep aspect ratio
            scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.emoji_label.setPixmap(scaled_pixmap)
            self.emoji_label.setText("")  # Clear any previous emoji text
        else:
            self.emoji_label.setText("❌")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

