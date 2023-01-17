import pygame


class TrafficLight:

    def __init__(self, light_id, position="horizontal", light_times_dict=None, status=None, countdown=0,
                 internal_clock= 0):

        self.id = light_id  # Used to identify which signaling device we are referring to.

        self.position = position  # Used to differentiate between horizontal and vertical lights, which act antagonistic.

        self.light_times_dict = light_times_dict  # How should the default light cycle look like counted in ticks.

        if self.light_times_dict is None:  # Used in order to eliminate a mutable argument.
            self.light_times_dict = {"red": 4*120, "yellow_to_green": 1*120, "green": 4*120, "yellow_to_red": 1*120}

        self.status = status  # Used in case we wish to manually enforce a certain starting light composition.

        self.countdown = countdown   # Used to synchronize light changes

        self.internal_clock = internal_clock  # Used to specify when the check starts

    def return_status(self):  # Returns current light status.
        return self.status

    def current_countdown(self):  # Returns current countdown.
        return self.countdown

    def return_id(self):  # Returns id of a device.
        return self.id

    def return_position(self):  # Returns whether the light is vertical or horizontal.
        return self.position

    def return_light_times(self):  # Returns dict with light times.
        return self.light_times_dict

    def begin_cycle(self):  # Begins the life of a signaling device.
        if self.status is None:
            self.status = "green"

    def next(self):  # Switch to next colour in cycle.
        order = ["red", "yellow_to_green", "green", "yellow_to_red"]
        current_position_in_cycle = order.index(self.status)
        try:
            self.status = order[current_position_in_cycle+1]
        except IndexError:
            self.status = "red"
        self.countdown = self.light_times_dict[self.status]
        return self.status

    def update(self):  # Updates the device with current time and changes its state based upon its passage.
        self.check_flag = 0
        self.countdown = self.countdown - 1
        if self.countdown == 0:
            self.next()

    def render(self):  # Returns its state as an adequately coloured square in pygame friendly object.
        signaling_device_image = pygame.Surface((25, 25))
        try:
            signaling_device_image.fill(self.status)
        except ValueError:
            signaling_device_image.fill("yellow")
        return signaling_device_image

    def change_light_times(self, new_data): # Changes the light time
        for key in new_data:
            if key in self.light_times_dict:
                self.light_times_dict[key] = new_data[key]


def create_signalisation(): # Utility fucntion to create default set of signaling devices.
    test_light_south = TrafficLight(light_id="south", position="vertical", status="green", countdown=5)
    test_light_east = TrafficLight(light_id="east", status="red", countdown=5)
    test_light_north = TrafficLight(light_id="north", position="vertical", status="green", countdown=5)
    test_light_west = TrafficLight(light_id="west", status="red", countdown=5)
    signalisation = (test_light_south, test_light_east, test_light_north, test_light_west)
    return signalisation


def update_all_lights(signalisation):  # Updates all signaling devices one by one.
    for signaling_device in signalisation:
        signaling_device.update()


def render_all_light(signalisation):  # Returns adequately coloured squares as gamepy objects packed with device's id.
    list_of_lights_images_with_cords = []
    for signaling_device in signalisation:
        list_of_lights_images_with_cords.append([signaling_device.render(), signaling_device.return_id()])
    return list_of_lights_images_with_cords


def optimize(data):  # Optimizes light lengths
    cars_total = 0
    for light in data:
        cars_total += data[light]
    weight_dict = {}
    for light in data:
        try:
            weight_dict[light] = float(data[light]) / float(cars_total)
        except ZeroDivisionError:
            weight_dict[light] = 0.25
    disposable_time = (10 - 4)  # time of a full cycle
    t_ver = 1
    t_hor = 1
    for light in weight_dict:
        if light == "north" or light == "south":
            t_ver += weight_dict[light] * disposable_time
        else:
            t_hor += weight_dict[light] * disposable_time
    new_times_dict = {"horizontal": t_hor, "vertical": t_ver}
    return new_times_dict


def substitute(new_times_dict, signalisation):  # Substitutes light timers for existing lights
    horizontal_timers = {"red": round(new_times_dict["vertical"]*120), "green": round(new_times_dict["horizontal"]*120)}
    vertical_timers = {"red": round(new_times_dict["horizontal"]*120), "green": round(new_times_dict["vertical"]*120)}
    for signaling_device in signalisation:
        if signaling_device.return_position() == "horizontal":
            signaling_device.change_light_times(horizontal_timers)
        else:
            signaling_device.change_light_times(vertical_timers)