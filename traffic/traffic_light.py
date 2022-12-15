# Goły szkic w którym na razie nic nie ma, w zasadzie tylko dowód dobrej woli.
class TrafficLight:

    def __init__(self, light_id, position="horizontal", light_times_dict=None, status=None, inner_time=0):

        self.id = light_id  # Used to identify which signaling device we are referring to

        self.position = position  # Used to differentiate between horizontal and vertical lights, which act antagonistic

        self.light_times_dict = light_times_dict  # How should the default light cycle look like counted in ticks

        if self.light_times_dict is None:  # Used in order to eliminate a mutable argument
            self.light_times_dict = {"red": 4, "yellow_to_green": 1, "green": 2, "yellow_to_red": 1}

        self.status = status  # Used in case we wish to manually enforce a certain starting light composition

        self.inner_time = inner_time

    def return_status(self):  # Returns current light status
        return self.status

    def begin_cycle(self):  # Begins the life of a signaling device
        if self.status is None:
            self.status = "green"
