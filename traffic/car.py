class Car:
    def __init__(self, id, acceleration, length, direction, max_v, starting_position, dt, height, width):
        self.id = id #car id
        self.acceleration = acceleration #acceleration in units/s
        self.length = length #length of car in m
        self.direction = direction #direction in which car is going
        self.max_v = max_v #max velocity of the car
        self.current_velocity = max_v #current velocity of the vehicle
        self.starting_position = starting_position[0]
        self.current_position = starting_position[1]
        self.dt = dt #step of the simulation
        self.height = height
        self.width = width
        self.crossed_intersection = False #flag that determines if the car crossed the intersection
        self.reached_destination = False #flag that determines if the car reached its destination
        self.car_orientation = 0

        self.car_starting_orientation()

    def __str__(self):
        return f"Car id={self.id} with acceleration {self.acceleration}, length {self.length} going {self.direction} going from {self.starting_position}.\n" \
               f"Current position: {self.current_position} and velocity: {self.current_velocity}. Orientation: {self.car_orientation}"

    def update_position(self):
        # updates position of the car depending on the direction, starting point and whether it has already crossed
        #the intersection
        if self.direction == 'ahead':
            if self.starting_position == 'south':
                self.current_position[1] -= self.current_velocity * self.dt
            elif self.starting_position == 'north':
                self.current_position[1] += self.current_velocity * self.dt
            elif self.starting_position == 'east':
                self.current_position[0] -= self.current_velocity * self.dt
            elif self.starting_position == 'west':
                self.current_position[0] += self.current_velocity * self.dt
        elif self.direction == 'left':
            if self.starting_position == 'south':
                if self.crossed_intersection == False:
                    self.current_position[1] -= self.current_velocity * self.dt
                else:
                    self.current_position[0] -= self.current_velocity * self.dt
            elif self.starting_position == 'north':
                if self.crossed_intersection == False:
                    self.current_position[1] += self.current_velocity * self.dt
                else:
                    self.current_position[0] += self.current_velocity * self.dt
            elif self.starting_position == 'east':
                if self.crossed_intersection == False:
                    self.current_position[0] -= self.current_velocity * self.dt
                else:
                    self.current_position[1] += self.current_velocity * self.dt
            elif self.starting_position == 'west':
                if self.crossed_intersection == False:
                    self.current_position[0] += self.current_velocity * self.dt
                else:
                    self.current_position[1] -= self.current_velocity * self.dt
        elif self.direction == 'right':
            if self.starting_position == 'south':
                if self.crossed_intersection == False:
                    self.current_position[1] -= self.current_velocity * self.dt
                else:
                    self.current_position[0] += self.current_velocity * self.dt
            elif self.starting_position == 'north':
                if self.crossed_intersection == False:
                    self.current_position[1] += self.current_velocity * self.dt
                else:
                    self.current_position[0] -= self.current_velocity * self.dt
            elif self.starting_position == 'east':
                if self.crossed_intersection == False:
                    self.current_position[0] -= self.current_velocity * self.dt
                else:
                    self.current_position[1] -= self.current_velocity * self.dt
            elif self.starting_position == 'west':
                if self.crossed_intersection == False:
                    self.current_position[0] += self.current_velocity * self.dt
                else:
                    self.current_position[1] += self.current_velocity * self.dt

    def has_crossed_intersection(self):
        x = 5 #temporary variable to fix visual bug where cars don't drive "on their lanes"
        if self.starting_position == 'north':
            if self.direction == 'right':
                if self.current_position[1] >= self.height/2 - x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1
                elif self.direction == 'left':
                    if self.current_position[1] >= self.height/2 + x:
                        self.crossed_intersection = True
                        if self.direction != 'ahead':
                            self.car_orientation *= -1

        elif self.starting_position == 'south':
            if self.direction == 'left':
                if self.current_position[1] <= self.height/2 - x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1
            elif self.direction == 'right':
                if self.current_position[1] <= self.height/2 + x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1

        elif self.starting_position == 'east':
            if self.direction == 'left':
                if self.current_position[0] <= self.width / 2 - x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1
            elif self.direction == 'right':
                if self.current_position[0] <= self.width / 2 + x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1

        elif self.starting_position == 'west':
            if self.direction == 'left':
                if self.current_position[0] >= self.width / 2 + x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1
            elif self.direction == 'right':
                if self.current_position[0] >= self.width / 2 - x:
                    self.crossed_intersection = True
                    if self.direction != 'ahead':
                        self.car_orientation *= -1

    def has_reached_destination(self):
        #check if the car has reached its destination (drove out of the map)
        if self.starting_position == 'north':
            if self.direction == 'ahead':
                if self.current_position[1] > self.height:
                    self.reached_destination = True
            elif self.direction == 'left':
                if self.current_position[0] > self.width:
                    self.reached_destination = True
            elif self.direction == 'right':
                if self.current_position[0] < 0:
                    self.reached_destination = True
        elif self.starting_position == 'south':
            if self.direction == 'ahead':
                if self.current_position[1] < 0:
                    self.reached_destination = True
            elif self.direction == 'left':
                if self.current_position[0] < 0:
                    self.reached_destination = True
            elif self.direction == 'right':
                if self.current_position[0] > self.width:
                    self.reached_destination = True
        elif self.starting_position == 'west':
            if self.direction == 'ahead':
                if self.current_position[0] > self.width:
                    self.reached_destination = True
            elif self.direction == 'left':
                if self.current_position[1] < 0:
                    self.reached_destination = True
            elif self.direction == 'right':
                if self.current_position[1] > self.height:
                    self.reached_destination = True
        elif self.starting_position == 'east':
            if self.direction == 'ahead':
                if self.current_position[0] < 0:
                    self.reached_destination = True
            elif self.direction == 'left':
                if self.current_position[1] > self.height:
                    self.reached_destination = True
            elif self.direction == 'right':
                if self.current_position[1] < 0:
                    self.reached_destination = True

    def car_starting_orientation(self):
        #determines car starting orientation (horizontal = 1 or vertical = -1)
        if self.starting_position in ('south', 'north'):
            self.car_orientation = -1
        else:
            self.car_orientation = 1
    def update(self):
        #update velocity
        if self.current_velocity == self.max_v:
            pass
        else:
            self.current_velocity += self.acceleration * self.dt

        #check if the car crossed intersection and update its position; additionally check if char reached its desti-
        #nation
        if not self.crossed_intersection:
            self.has_crossed_intersection()
        self.update_position()
        self.has_reached_destination()