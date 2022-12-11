from traffic import *
import pygame
import random

cars = []
current_free_car_id = 0#current car id that can be used to generate a new car

def generate_traffic(id = current_free_car_id): #randomly generate a car
    acceleration = random.randint(12, 18) * 0.5
    length = round(random.randint(40, 55) * 0.1, 1)
    direction = ['ahead', 'left', 'ahead','right', 'ahead', 'ahead'][random.randint(0,5)]
    max_v = float(random.randint(90, 120))

    cars.append(car.Car(id,acceleration, length, direction, max_v))
