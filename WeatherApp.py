from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon, QMovie
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from typing import Dict
import requests
import sys

class WeatherApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.SetMainWindowStyle()
        self.initGUI()
    
    
    def SetMainWindowStyle(self) -> None:
        self.setWindowIcon(QIcon("Items/rain_.png"))
        self.setWindowTitle("Weather App")
        self.setGeometry(500, 200, 600, 400)
        
    
    def initGUI(self) -> None:
        self.Create_variables()
        self.set_window_layout()
        self.set_style()
        
        self.get_weather_button.clicked.connect(self.display_weather)
        self.input_box.returnPressed.connect(self.display_weather)
    
    
    def Create_variables(self) -> None:
        self.city_label = QLabel("Enter City Name: ", self)
        self.weather_label = QLabel("Sunny",self)
        self.temperature_label = QLabel(f"100°C 🌤️",self)
        
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Python City")
        self.get_weather_button = QPushButton("Get Weather",self)
    
    
    def set_window_layout(self) -> None:
        vbox = QVBoxLayout(self)
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.input_box)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.weather_label)
        vbox.addWidget(self.temperature_label)
        
        self.setLayout(vbox)
    
    
    
    def set_style(self) -> None:
        self.city_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.city_label.setObjectName("city_label")
        self.input_box.setObjectName("input_box")
        self.get_weather_button.setObjectName("get_weather_button")
        self.weather_label.setObjectName("weather_label")
        self.temperature_label.setObjectName("temperature_label")
        
        
        self.setStyleSheet("""
                           QLabel {
                               font-size: 30px;
                           }
                           QLabel, QPushButton {
                               font-family: cilibri;
                           }
                           QLabel#city_label {
                               font-size: 30px;
                               font-weight: bold;
                           }
                           QLineEdit#input_box {
                               font-size: 30px;
                               layout
                           }
                           QPushButton#get_weather_button {
                               font-size: 20px;
                               font-weight: bold;
                           }
                           """)
    
    
    def display_weather(self) -> None:
        city_name = self.input_box.text().strip()
        if city_name:
            weather_infos = self.get_weather(city_name)
            if weather_infos:
                kevin = weather_infos['main']['temp']
                weather = weather_infos['weather'][0]['main']
                weather_id = int(weather_infos['weather'][0]['id'])
                celsius = kevin - 273.15

                emoji = self.display_weather_emoji(weather_id)
                self.weather_label.setText(f"{weather}")
                self.temperature_label.setText(f"{celsius:.0f}°C {emoji}")
        else:
            self.display_error("Please enter a city name")
        
    
    
    def get_weather(self, city_name: str) -> Dict[str, str]:
        key = ""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}"
        try:
            infos = requests.get(url)
            infos.raise_for_status()
            return infos.json()
        except requests.exceptions.HTTPError as http_error:
            match infos.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess denied")
                case 404:
                    self.display_error("Not Found\nCity not found")
                case 500:
                    self.display_error("Internal Server Error\nThe server has encountered a situation it does not know how to handle")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nResponse timedout")
                case _:
                    self.display_error(f"An unexpected error happend\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nRequest timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nCheck URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")
            
            
    def display_error(self, message: str) -> None:
        self.weather_label.setText(f"Error: {message}")
        self.temperature_label.setText("")
        
    
    @staticmethod
    def display_weather_emoji(weather_id: int) -> str:
        match weather_id:
            case _ if 200 <= weather_id <= 232:
                return "⛈️"
            case _ if 300 <= weather_id <= 321:
                return "☔"
            case _ if 500 <= weather_id <= 531:
                return "🌧️"
            case _ if 600 <= weather_id <= 622:
                return "☃️"
            case _ if weather_id == 800:
                return "☀️"
            case _ if 801 <= weather_id <= 804:
                return "☁️"
            case _:
                return "🌤️"
    
    
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.close()
                
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather = WeatherApp()
    weather.show()
    sys.exit(app.exec())
