class Trip:
    """
    docstring for Trip
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):

        if type(acceptable_modes) is not list:
            self._acceptable_modes = [acceptable_modes]
        else:
            self._acceptable_modes = acceptable_modes
        self._start = start
        self._end = end
        self._departure_time = departure_time
        self._arrival_time = arrival_time

    def get_acceptable_modes(self):
        return self._acceptable_modes

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_departure_time(self):
        return self._departure_time

    def get_arrival_time(self):
        return self._arrival_time
