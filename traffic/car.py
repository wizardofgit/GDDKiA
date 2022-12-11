class Car:
    def __init__(self, id, acceleration, length, direction):
        self.id = id #id auta
        self.acceleration = acceleration #przyspieszenie w km/s
        self.length = length #dlugosc auta
        self.direction = direction #kierunek w jaki jedzie auto

    def __str__(self):
        return f"Car with id {self.id} with acceleration {self.acceleration}, length {self.length} going {self.direction}"