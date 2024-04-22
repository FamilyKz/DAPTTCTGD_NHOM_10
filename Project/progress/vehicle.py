import os
from config import Vehicle_config


class Main_vehicle:
    LIST_VEHICLE: int = [[0] * 5 for _ in range(Vehicle_config.NUMBER)]
    LIST_NAME_VEHICLE: int = os.listdir("./pic/Vehicle_speed")


