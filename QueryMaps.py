from datetime import datetime
import googlemaps
import keys
import pprint


class QueryMaps:
    def __init__(self, start, end, mode, departure_time=None, arrival_time=None):
        self._gmaps = googlemaps.Client(keys.gmaps)
        self._start = start
        self._end = end
        self._departure_time = departure_time
        self._arrival_time = arrival_time
        self._pprinter = pprint.PrettyPrinter(indent=4)
        self._dir_result = None
        self.update_query(start, end, mode, departure_time, arrival_time)

    def get_departure_time(self):
        return self._departure_time

    def get_arrival_time(self):
        return self._arrival_time

    def get_directions_result(self):
        return self._dir_result

    def get_end(self):
        return self._end

    def get_start(self):
        return self._start

    def print_directions(self):
        self._pprinter.pprint(self._dir_result)

    def update_query(self, start, end, mode, departure_time=None, arrival_time=None):
        if departure_time is None and arrival_time is None:
            departure_time = datetime.now()
        self._dir_result = self._gmaps.directions(start, end, mode, departure_time=departure_time)[0]
