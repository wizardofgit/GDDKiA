from traffic.traffic_light import *
from traffic.car import Car
import pygame
import random
from sys import exit
import json

dt = 0.01 #step of the simulation in seconds
width, height = 1280, 720 #width and height of the window
starting_positions_cord = {'north': (width/2 - 5, 0),
                           'south': (width/2 + 5, height),
                           'east': (width, height/2 - 5),
                           'west': (0, height/2 + 5)}  #starting coordinates for different directions
car_queues = {'east_right': [], 'east_left': [],
              'west_right': [], 'west_left': [],
              'south_down': [], 'south_up': [],
              'north_down': [], 'north_up': []} #contains the ids of cars that are in a certain segment of the road
status_log = {} #status of all vehicles
cars = [] #list of existing cars (i.e. being displayed)
current_free_car_id = 0 #current car id that can be used to generate a new car
cars_passed = 0 #how many cars has entered and cleared the junction
time_elapsed = 0.0 #how much time has passed since the start of the simulation
time_threshold = 0 #after certain threshold new cars will be generated
time_threshold_step = 2 #time_threshold will be updated, so that cars are generated every time_threshold_step seconds
minimum_cars_passed = 10 #number of cars which passed after which the simulation ends
t, t_step = 0, 0.01 #variables controlling how often info is logged

sig = create_signalisation()  # Creating 4 signaling devices and their coordinates
light_cords = {'north': [width/2 - 30 , height/2 - 30],
               'south': [width/2 + 15 , height/2 + 15],
               'east': [width/2 + 15 , height/2 - 30],
               'west': [width/2 - 30 , height/2 + 15]}

def generate_traffic(direction = None, selected_starting_point = None): #randomly generates a car
    id = current_free_car_id
    #acceleration = random.randint(14, 18) * 0.5
    acceleration = 9
    length = round(random.randint(40, 55) * 0.1, 1)
    if direction == None:
        direction = ['ahead', 'left', 'ahead','right', 'ahead', 'ahead'][random.randint(0,5)]
    #max_v = float(random.randint(100, 160))
    max_v = 140
    if selected_starting_point == None:
        selected_starting_point = list(starting_positions_cord.keys())[random.randint(0, 3)]
    starting_position = [selected_starting_point, starting_positions_cord[selected_starting_point]] #include list consisting of starting position and its coordinates
    print(starting_positions_cord)
    print(starting_position)
    cars.append(Car(id, acceleration, length, direction, max_v, starting_position, dt, height, width))

def show_car_info(): #prints info about all cars or car with certain id
    for car in cars:
        print("Time elapsed: ",time_elapsed)
        if 'car_' + str(car.id) in status_log:
            status_log['car_' + str(car.id)].append(car.__str__())
        else:
            status_log['car_' + str(car.id)] = []
            status_log['car_' + str(car.id)].append(car.__str__())
        print(car)
    print('')

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
car_id_text = pygame.font.Font(None, 20)
car_on_screen_text = pygame.font.Font(None, 50)

while True:
    for event in pygame.event.get():    #check what user did
        if event.type == pygame.QUIT:   #if user clicked 'x' (aka quit) in window
            pygame.quit()
            print("Average car flow: ", cars_passed / time_elapsed * 3600, " per hour")
            with open('status_log.json', 'w') as f: #saves status log as a json file
                f.write(json.dumps(status_log))
            exit()  #stop the app
    if cars_passed >= minimum_cars_passed:
        pygame.quit()
        print("Average car flow: ", cars_passed / time_elapsed * 3600, " per hour")
        with open('status_log.json', 'w') as f: #saves status log as a json file
            f.write(json.dumps(status_log))
        exit()  # stop the app

    #update images on screen
    screen.blit(background, (0,0))
    screen.blit(map_center, (width/2, height/2))
    screen.blit(road_horizontal, (0, height/2 - 5))
    screen.blit(road_vertical, (width/2 - 5, 0))
    text_image = text.render(str(round(time_elapsed, 2)), True, 'White')
    screen.blit(text_image, (0,0))
    car_on_screen_text_image = car_on_screen_text.render(str(len(cars)), True, 'White')
    screen.blit(car_on_screen_text_image, (0,30))
    
    # Update lights
    update_all_lights(sig)
    current_lights_list = render_all_light(sig)
    for signaling_device_and_cord in current_lights_list:
        screen.blit(signaling_device_and_cord[0], light_cords[signaling_device_and_cord[1]])
        
    #generates another car after certain in-simulation seconds elapsed
    if time_elapsed > time_threshold:
        generate_traffic()
        current_free_car_id += 1
        time_threshold += time_threshold_step

    if time_elapsed > t:
        t += t_step
        show_car_info()

    # update the parameters of every car on the road; check if cars are to be deleted
    cars_to_be_deleted = []
    for car in cars:
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
            id_image = car_id_text.render(str(car.id), True, 'Black')
            screen.blit(car_image_horizontal, car.current_position)
            screen.blit(id_image, car.current_position)
        else:
            screen.blit(car_image_vertical, car.current_position)
            id_image = car_id_text.render(str(car.id), True, 'Black')
            screen.blit(id_image, car.current_position)

    time_elapsed += dt
    pygame.display.update() #update the screen
    clock.tick(60) #simulation should run at no more than said amount of ticks per second
