from datetime import datetime
import googlemaps
import keys
import pprint
from Trip import Trip


class QueryMaps(Trip):
    def __init__(self, start, end, mode, departure_time=None, arrival_time=None):
        Trip.__init__(self, start, end, mode, departure_time, arrival_time)
        self._gmaps = googlemaps.Client(keys.gmaps)
        self._pprinter = pprint.PrettyPrinter(indent=4)
        self._dir_result = None
        self.update_query(start, end, mode, departure_time, arrival_time)

    def get_directions_result(self):
        return self._dir_result

    def print_directions(self):
        self._pprinter.pprint(self._dir_result)

    def update_query(self, start, end, mode, departure_time=None, arrival_time=None):
        if departure_time is None and arrival_time is None:
            departure_time = datetime.now()
        self._dir_result = self._gmaps.directions(start, end, mode, departure_time=departure_time)[0]
