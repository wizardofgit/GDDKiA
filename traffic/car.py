class Car:
    def __init__(self, id, acceleration, length, direction, max_v):
        self.id = id #car id
        self.acceleration = acceleration #acceleration in km/s
        self.length = length #length of car in m
        self.direction = direction #direction in which car is going
        self.max_v = max_v #max velocity of the car

    def __str__(self):
        return f"Car id={self.id} with acceleration {self.acceleration}, length {self.length} going {self.direction}"