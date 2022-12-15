
class TrafficLight:

    def __init__(self, light_id, position="horizontal", light_times_dict=None, status=None, countdown=0):

        self.id = light_id  # Used to identify which signaling device we are referring to

        self.position = position  # Used to differentiate between horizontal and vertical lights, which act antagonistic

        self.light_times_dict = light_times_dict  # How should the default light cycle look like counted in ticks

        if self.light_times_dict is None:  # Used in order to eliminate a mutable argument
            self.light_times_dict = {"red": 4*120, "yellow_to_green": 1*120, "green": 4*120, "yellow_to_red": 1*120}

        self.status = status  # Used in case we wish to manually enforce a certain starting light composition

        self.countdown = countdown  # Used as a substite for the passage of time in simulation

    def return_status(self):  # Returns current light status
        return self.status

    def begin_cycle(self):  # Begins the life of a signaling device
        if self.status is None:
            self.status = "green"
            
    def next(self):
        order = ["red", "yellow_to_green", "green", "yellow_to_red"]
        current_position_in_cycle = order.index(self.status)
        try:
            self.status = order[current_position_in_cycle+1]
        except IndexError:
            self.status = "red"
        self.countdown = self.light_times_dict[self.status]
            
    def update(self):  # Updates the device with current time and changes it's state based upon it's passage.
        self.countdown -= 1
        if self.countdown == 0:
            self.next
