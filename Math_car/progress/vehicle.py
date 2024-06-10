import os


class Vehicle_config:
    NUMBER: int = 10 
    DELAY: int = 100


class Main_vehicle:
    LIST_VEHICLE: int = [[0] * 6 for _ in range(Vehicle_config.NUMBER)]
    LIST_NAME_VEHICLE: int = os.listdir("./pic/Vehicle_speed")


