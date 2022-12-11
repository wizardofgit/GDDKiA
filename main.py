from traffic import *
import pygame
import random
from sys import exit

dt = 0.01 #step of the simulation in seconds
width, height = 1280, 720 #width and height of the window
starting_positions_cord = {'north': [width/2 - 5, 0],
                           'south': [width/2 + 5, height],
                           'east': [width, height/2 - 5],
                           'west': [0, height/2 + 5]}  #starting coordinates for different directions
cars = [] #list of existing cars (i.e. being displayed)
current_free_car_id = 0 #current car id that can be used to generate a new car
cars_passed = 0 #how many cars has entered and cleared the junction
time_elapsed = 0.0 #how much time has passed since the start of the simulation
time_threshold = 0 #after certain threshold new cars will be generated

def generate_traffic(): #randomly generates a car
    id = current_free_car_id
    acceleration = random.randint(12, 18) * 0.5
    length = round(random.randint(40, 55) * 0.1, 1)
    direction = ['ahead', 'left', 'ahead', 'ahead','right', 'ahead', 'ahead'][random.randint(0,6)]
    max_v = float(random.randint(90, 160))
    selected_starting_point = random.randint(0, 3)
    starting_position = [list(starting_positions_cord.keys())[selected_starting_point],
                         starting_positions_cord[list(starting_positions_cord.keys())[selected_starting_point]]] #include list consisting of starting position and
                                                                                                                 #its coordinates

    cars.append(car.Car(id, acceleration, length, direction, max_v, starting_position, dt, height, width))
    print(cars[id])

#create simple plain color road and car images
road_horizontal = pygame.Surface((width, 20))
road_horizontal.fill('White')
road_vertical = pygame.Surface((20, height))
road_vertical.fill('White')
car_image_horizontal = pygame.Surface((25, 10))
car_image_horizontal.fill('Red')
car_image_vertical = pygame.Surface((10, 25))
car_image_vertical.fill('Red')
background = pygame.Surface((width,height))
background.fill('Black')

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Symulacja skrzyżowania")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():    #check what user did
        if event.type == pygame.QUIT:   #if user clicked 'x' (aka quit) in window
            pygame.quit()
            print("Average car flow: ", cars_passed / time_elapsed)
            exit()  #stop the app

    #update images on screen
    screen.blit(background, (0,0))
    screen.blit(road_horizontal, (0, height/2 - 5))
    screen.blit(road_vertical, (width/2 - 5, 0))

    #generates another car after certain in-simulation seconds elapsed
    if time_elapsed > float(time_threshold):
        generate_traffic()
        current_free_car_id += 1
        time_threshold += 2

    #update the parameters of every car on the road; display all the cars
    for car in cars:
        car.update()
        #print(car)
        if car.reached_destination:
            cars_passed += 1
            del car

    for car in cars:
        if car.car_orientation == 1:
            screen.blit(car_image_horizontal, tuple(car.current_position))
        else:
            screen.blit(car_image_vertical, tuple(car.current_position))

    time_elapsed += dt
    pygame.display.update() #update the screen
    clock.tick(120) #simulation should run at no more than said amount of ticks per second