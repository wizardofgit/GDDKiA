from traffic.traffic_light import *
from traffic.car import Car
import pygame
import random
from sys import exit
import math

dt = 0.01 #step of the simulation in seconds
width, height = 1280, 720 #width and height of the window
starting_positions_cord = {'north': (width/2 - 5, 0),
                           'south': (width/2 + 5, height),
                           'east': (width, height/2 - 5),
                           'west': (0, height/2 + 5)}  #starting coordinates for different directions
car_queues = {'east_right': [], 'east_left': [],
              'west_right': [], 'west_left': [],
              'south_down': [], 'south_up': [],
              'north_down': [], 'north_up': []} #contains the cars that are in a certain segment of the road
optimization_auxiliary_queue = {"north": [], "south": [], "west": [], "east": []}
status_log = {} #status of all vehicles
cars = [] #list of existing cars (i.e. being displayed)
current_free_car_id = 0 #current car id that can be used to generate a new car
cars_passed = 0 #how many cars has entered and cleared the junction
time_elapsed = 0.0 #how much time has passed since the start of the simulation
time_threshold = 0 #after certain threshold new cars will be generated
time_threshold_step = 1 #time_threshold will be updated, so that cars are generated every time_threshold_step seconds
minimum_cars_passed = 100 #number of cars which passed after which the simulation ends
optimization_interval = 2  # Amount of esconds between optimizer scans
t, t_step = 0, 0.01 #variables controlling how often info is logged

sig = create_signalisation()  # Creating 4 signaling devices and their coordinates
light_cords = {'north': [width/2 - 30 , height/2 - 30],
               'south': [width/2 + 15 , height/2 + 15],
               'east': [width/2 + 15 , height/2 - 30],
               'west': [width/2 - 30 , height/2 + 15]}


def update_auxiliary_queues(cars, list_of_queues):
    for queue in list_of_queues:
        list_of_queues[queue] = []
    for vehicle in cars:
        car_id = vehicle.return_id()
        queue_id = vehicle.return_queue()
        if queue_id in list_of_queues:
            list_of_queues[str(queue_id)].append(car_id)
    current_totals = {}
    for queue in list_of_queues:
        current_totals[queue] = len(list_of_queues[queue])
    return current_totals

def light_optimization_routine(cars, car_queues):  #  Whenever southern light does full rotation lights calibrate themselves.
    current = update_auxiliary_queues(cars, car_queues)
    print(car_queues)
    print(current)
    solution = optimize(current)
    print(solution)
    substitute(solution, sig)
    for device in sig:
        print(device.return_id(), device.return_light_times())


def generate_traffic(direction = None, selected_starting_point = None): #randomly generates a car
    id = current_free_car_id
    acceleration = random.randint(20, 40) * 0.5
    #acceleration = 9
    #length = round(random.randint(40, 60) * 0.1, 1)
    length = 4.5
    if direction == None:
        direction = ['ahead', 'left', 'ahead','right', 'ahead', 'ahead'][random.randint(0,5)]
    max_v = float(random.randint(100, 160))
    #max_v = 140
    if selected_starting_point == None:
        selected_starting_point = list(starting_positions_cord.keys())[random.randint(0, 3)]
    starting_position = [selected_starting_point, starting_positions_cord[selected_starting_point]] #include list consisting of starting position and its coordinates
    # print(starting_positions_cord)
    # print(starting_position)
    cars.append(Car(id, acceleration, length, direction, max_v, starting_position, dt, height, width, queue=str(selected_starting_point)))


def show_car_info(): #prints info about all cars or car with certain id
    print("Time elapsed: ", time_elapsed)
    for car in cars:
        if 'car_' + str(car.id) in status_log:
            status_log['car_' + str(car.id)].append(car.__str__())
        else:
            status_log['car_' + str(car.id)] = []
            status_log['car_' + str(car.id)].append(car.__str__())
        print(car)
    print('')

def distance_to_light(car, light):
    if light == 'south':
        return abs(car.current_position[1] - light_cords['south'][1])
    elif light == 'north':
        return abs(light_cords['north'][1] - car.current_position[1])
    elif light == 'east':
        return abs(car.current_position[0] - light_cords['east'][0])
    else:
        return abs(light_cords['west'][0] - car.current_position[0])
def sort_cars(l, p, r = False):    #sorts list l using parameter p: 0 for sorting by x-coordinate and 1 for y-coordinate
                                   # as well as parameter r that tells if the list is to be reversed or not
    l.sort(key = lambda x: x.current_position[p], reverse = r)
    return l
def check_car_distance():
    car_queues = {'east_right': [], 'east_left': [],
              'west_right': [], 'west_left': [],
              'south_down': [], 'south_up': [],
              'north_down': [], 'north_up': []} #resets the info about car segments
    cars_to_stop = []
    cars_to_go = []

    for car in cars:
        car_queues[car.road_segment].append(car) #updates the car_ques with car object

    for key in car_queues.keys():
        car_list = car_queues[key]  #has car objects on selected road segment

        if key == 'south_up': #sorts car list according to the segment of the road
            car_list = sort_cars(car_list, 1)
        elif key == 'north_down':
            car_list = sort_cars(car_list, 1, True)
        elif key == 'south_down':
            car_list = sort_cars(car_list, 1, True)
        elif key == 'north_up':
            car_list = sort_cars(car_list, 1)
        elif key == 'west_right':
            car_list = sort_cars(car_list, 0, True)
        elif key == 'west_left':
            car_list = sort_cars(car_list, 0,)
        elif key == 'east_right':
            car_list = sort_cars(car_list, 0, True)
        elif key == 'east_left':
            car_list = sort_cars(car_list, 0)

        y = 15  # variable to fix stopping distance from light so they dont stop in the middle of the intersection or too soon
        if len(car_list) > 1:
            for car_nr in range(len(car_list) - 1): #checks if the car is going to hit the car behind
                if math.sqrt((car_list[car_nr].current_position[0] - car_list[car_nr + 1].current_position[0])**2 + (car_list[car_nr].current_position[1] - car_list[car_nr + 1].current_position[1])**2) <= car_list[car_nr + 1].stopping_distance + y:
                    cars_to_stop.append(car_list[car_nr + 1].id)
                else:
                    cars_to_go.append(car_list[car_nr + 1].id)

        if key in ['south_up', 'east_left', 'west_right', 'north_down'] and len(car_list) > 0:    #checks if the car can cross the intersection (checks lights)
            if key == 'south_up':
                if sig[0].status == 'green' or car_list[0].current_position[1] - car_list[0].stopping_distance >= light_cords['south'][1] - y:
                    cars_to_go.append(car_list[0].id)
                elif sig[0].status == 'yellow_to_red' and car_list[0].current_position[1] - car_list[0].stopping_distance <= light_cords['south'][1] - y:
                    cars_to_go.append(car_list[0].id)
                else:
                    cars_to_stop.append(car_list[0].id)
            elif key == 'north_down':
                if sig[2].status == 'green' or car_list[0].current_position[1] + car_list[0].stopping_distance <= light_cords['north'][1] + y:
                    cars_to_go.append(car_list[0].id)
                elif sig[2].status == 'yellow_to_red' and car_list[0].current_position[1] + car_list[0].stopping_distance >= light_cords['north'][1] + y:
                    cars_to_go.append(car_list[0].id)
                else:
                    cars_to_stop.append(car_list[0].id)
            elif key == 'east_left':
                if sig[1].status == 'green' or car_list[0].current_position[0] - car_list[0].stopping_distance >= light_cords['east'][0] - y:
                    cars_to_go.append(car_list[0].id)
                elif sig[1].status == 'yellow_to_red' and car_list[0].current_position[0] - car_list[0].stopping_distance <= light_cords['east'][0] - y:
                    cars_to_go.append(car_list[0].id)
                else:
                    cars_to_stop.append(car_list[0].id)
            elif key == 'west_right':
                if sig[3].status == 'green' or car_list[0].current_position[0] + car_list[0].stopping_distance <= light_cords['west'][0] + y:
                    cars_to_go.append(car_list[0].id)
                elif sig[3].status == 'yellow_to_red' and car_list[0].current_position[0] + car_list[0].stopping_distance >= light_cords['west'][0] + y:
                    cars_to_go.append(car_list[0].id)
                else:
                    cars_to_stop.append(car_list[0].id)
        elif len(car_list) > 0:
            cars_to_go.append(car_list[0].id)

    # for key in car_queues.keys():
    #     print(f"{key} {list(map(lambda x: x.id, car_queues[key]))}")

    for car in cars:
        if car.id in cars_to_go:
            car.instruction = 'go'
        elif car.id in cars_to_stop:
            car.instruction = 'stop'



#create simple plain color road and car images
road_horizontal = pygame.Surface((width, 20))
road_horizontal.fill('White')
road_vertical = pygame.Surface((20, height))
road_vertical.fill('White')
car_image_horizontal_stop = pygame.Surface((25, 10))
car_image_horizontal_stop.fill('Red')
car_image_vertical_stop = pygame.Surface((10, 25))
car_image_vertical_stop.fill('Red')
car_image_horizontal_go = pygame.Surface((25, 10))
car_image_horizontal_go.fill('Green')
car_image_vertical_go = pygame.Surface((10, 25))
car_image_vertical_go.fill('Green')
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
cars_passed_text = pygame.font.Font(None, 50)

while True:
    for event in pygame.event.get():    #check what user did
        if event.type == pygame.QUIT:   #if user clicked 'x' (aka quit) in window
            pygame.quit()
            print("Average car flow:", cars_passed / time_elapsed * 3600, "per hour")
            exit()  #stop the app
    if cars_passed >= minimum_cars_passed:
        pygame.quit()
        print("Average car flow:", cars_passed / time_elapsed * 3600, "per hour")
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
    cars_passed_test_image = cars_passed_text.render(str(cars_passed), True, 'White')
    screen.blit(cars_passed_test_image, (0, 60))
    
    # Update lights
    update_all_lights(sig)
    current_lights_list = render_all_light(sig)
    for signaling_device_and_cord in current_lights_list:
        screen.blit(signaling_device_and_cord[0], light_cords[signaling_device_and_cord[1]])
    if (round(time_elapsed, 1) % optimization_interval)  == 0:
        light_optimization_routine(cars, optimization_auxiliary_queue)
        
    #generates another car after certain in-simulation seconds elapsed
    if time_elapsed > time_threshold:
        generate_traffic()
        current_free_car_id += 1
        time_threshold += time_threshold_step

    if time_elapsed > t:
        t += t_step
        # show_car_info()

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

    check_car_distance()
    #display all the cars
    for car in cars:
        if car.car_orientation == 1:
            id_image = car_id_text.render(str(car.id), True, 'Black')
            if car.instruction == 'stop':
                screen.blit(car_image_horizontal_stop, car.current_position)
            else:
                screen.blit(car_image_horizontal_go, car.current_position)
            screen.blit(id_image, car.current_position)
        else:
            if car.instruction == 'stop':
                screen.blit(car_image_vertical_stop, car.current_position)
            else:
                screen.blit(car_image_vertical_go, car.current_position)
            id_image = car_id_text.render(str(car.id), True, 'Black')
            screen.blit(id_image, car.current_position)

    time_elapsed += dt
    pygame.display.update() #update the screen
    clock.tick(120) #simulation should run at no more than said amount of ticks per second
