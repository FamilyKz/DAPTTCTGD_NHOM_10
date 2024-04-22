from config import Weather_config
import os

class Main_Weather:
    LIST_WEATHER: int = [[0] * 3 for _ in range(Weather_config.NUMBER)]
    LIST_NAME_WEATHER: int = os.listdir('./pic/Weather')
