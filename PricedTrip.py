from __future__ import print_function

import json
from QueryParser import QueryParser
from Trip import Trip


class PricedTrip(Trip):
    """
    docstring for Trip
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        Trip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)

        self._directions = {}
        self._distance = None
        self._duration = 0.0
        self._price_range = [None, None]
        self._start_location = {'lat': None, 'lng': None}
        self._end_location = {'lat': None, 'lng': None}

    def get_directions(self):
        return self._directions.copy()

    def get_directions_json(self):
        return json.dumps(self.get_directions())

    def get_distance(self):
        return self._distance

    def get_duration(self):
        return self._duration

    def get_end_location(self):
        return self._end_location

    def get_price_range(self):
        return self._price_range

    def get_start_location(self):
        return self._start_location

    def _parse_loc_dict(self, loc_dict):
        return loc_dict['lat'], loc_dict['lng']

    def query_parse_factory(self, mode):
        return QueryParser(self._start, self._end, mode, self._departure_time, self._arrival_time)

    def set_directions(self, directions):
        self._directions = directions

    def set_distance(self, distance):
        self._distance = distance

    def set_duration(self, duration):
        self._duration = duration

    def set_price_range(self, price_range):
        """
        Price range is always (low, high) where low <= high.
        :param price_range:
        :return:
        """
        assert isinstance(price_range, tuple) and len(price_range) == 2 and price_range[0] <= price_range[1], "Ill formatted price range"
        self._price_range = price_range

    def set_start_location(self, lat, lng):
        self._start_location['lat'] = lat
        self._start_location['lng'] = lng

    def set_end_location(self, lat, lng):
        self._end_location['lat'] = lat
        self._end_location['lng'] = lng

    def set_end_loc_from_dict(self, end_dict):
        lat, lng = self._parse_loc_dict(end_dict)
        self.set_end_location(lat, lng)

    def set_start_loc_from_dict(self, start_dict):
        lat, lng = self._parse_loc_dict(start_dict)
        self.set_start_location(lat, lng)
