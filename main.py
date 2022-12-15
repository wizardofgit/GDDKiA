from traffic.car import Car
import pygame
import random
from sys import exit

dt = 0.01 #step of the simulation in seconds
width, height = 1280, 720 #width and height of the window
starting_positions_cord = {'north': [width/2 - 5, 5],
                           'south': [width/2 + 5, height],
                           'east': [width, height/2 - 5],
                           'west': [5, height/2 + 5]}  #starting coordinates for different directions
car_queues = {'east_right': [], 'east_left': [],
              'west_right': [], 'west_left': [],
              'south_down': [], 'south_up': [],
              'north_down': [], 'north_up': []} #contains the ids of cars that are in a certain segment of the road
cars = [] #list of existing cars (i.e. being displayed)
current_free_car_id = 0 #current car id that can be used to generate a new car
cars_passed = 0 #how many cars has entered and cleared the junction
time_elapsed = 0.0 #how much time has passed since the start of the simulation
time_threshold = 0 #after certain threshold new cars will be generated
time_threshold_step = 2 #time_threshold will be updated, so that cars are generated every time_threshold_step seconds

def generate_traffic(direction = None, selected_starting_point = None): #randomly generates a car
    id = current_free_car_id
    acceleration = random.randint(14, 18) * 0.5
    length = round(random.randint(40, 55) * 0.1, 1)
    if direction == None:
        direction = ['ahead', 'left', 'ahead','right', 'ahead', 'ahead'][random.randint(0,5)]
    max_v = float(random.randint(100, 160))
    if selected_starting_point == None:
        selected_starting_point = random.randint(0, 3)
    starting_position = [list(starting_positions_cord.keys())[selected_starting_point],
                         starting_positions_cord[list(starting_positions_cord.keys())[selected_starting_point]]] #include list consisting of starting position and
                                                                                                                 #its coordinates

    cars.append(Car(id, acceleration, length, direction, max_v, starting_position, dt, height, width))

def show_car_info(id = None, start_printing = 1.00, step = 2.00): #prints info about all cars or car with certain id
    if id is None:
        if time_elapsed > start_printing:
            for car in cars:
                print(car, time_elapsed)
            start_printing += step
    else:
        if time_elapsed > start_printing:
            for car in cars:
                if car.id == id:
                    print(car)
            start_printing += step

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
map_center = pygame.Surface((1, 1))
map_center.fill('Blue')

#initalizing pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Symulacja skrzyżowania")
clock = pygame.time.Clock()
text = pygame.font.Font(None, 50)

generate_traffic()

while True:
    for event in pygame.event.get():    #check what user did
        if event.type == pygame.QUIT:   #if user clicked 'x' (aka quit) in window
            pygame.quit()
            print("Average car flow: ", cars_passed / time_elapsed * 3600, " per hour")
            exit()  #stop the app
    if len(cars) == 0 and time_elapsed > 5:
        pygame.quit()
        print("Average car flow: ", cars_passed / time_elapsed * 3600, " per hour")
        exit()  # stop the app

    #update images on screen
    screen.blit(background, (0,0))
    screen.blit(map_center, (width/2, height/2))
    screen.blit(road_horizontal, (0, height/2 - 5))
    screen.blit(road_vertical, (width/2 - 5, 0))
    text_image = text.render(str(round(time_elapsed, 2)), True, 'White')
    screen.blit(text_image, (0,0))

    #generates another car after certain in-simulation seconds elapsed
    if time_elapsed > time_threshold:
        generate_traffic()
        current_free_car_id += 1
        time_threshold += time_threshold_step

    #update the parameters of every car on the road; check if cars are to be deleted
    cars_to_be_deleted = []
    show_car_info()
    for i in range(len(cars)):
        car = cars[i]
        car.update()

        if car.reached_destination:
            cars_passed += 1
            cars_to_be_deleted.append(car.id)

    for car in cars:    #remove cars that has reached their destination
        if car.id in cars_to_be_deleted:
            cars.remove(car)

    #display all the cars
    for car in cars:
        if car.car_orientation == 1:
            screen.blit(car_image_horizontal, tuple(car.current_position))
        else:
            screen.blit(car_image_vertical, tuple(car.current_position))

    time_elapsed += dt
    pygame.display.update() #update the screen
    clock.tick(180) #simulation should run at no more than said amount of ticks per second