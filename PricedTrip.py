from QueryParser import QueryParser
from Trip import Trip


class PricedTrip(Trip):
    """
    docstring for Trip
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        Trip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)

        self._duration = 0.0
        self._distance = None
        self._price_range = [None, None]
        self._directions = None

    def get_directions(self):
        return self._directions

    def get_distance(self):
        return self._distance

    def get_duration(self):
        return self._duration

    def get_price_range(self):
        return self._price_range

    def quick_parse(self, mode):
        return QueryParser(self._start, self._end, mode, self._departure_time, self._arrival_time)

    def set_duration(self, duration):
        self._duration = duration
