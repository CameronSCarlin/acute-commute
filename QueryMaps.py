from datetime import datetime
import googlemaps
import keys
import pprint
from Trip import Trip


class QueryMaps(Trip):
    """
    Provides access to Google Maps API.
    """
    def __init__(self, start, end, mode, departure_time=None, arrival_time=None):
        """

        :param start (str or dict): Start location of trip
        :param end (str or dict): End location of trip
        :param mode (str): The mode of travel for the trip
        :param departure_time (str): Time of departure
        :param arrival_time (str): Time of arrival
        """
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
        """
        This method calls Google Maps to perform the search. Used in the constructor
        or as a public method to update the query without instantiating a new QueryMaps object.

        :param start: Start location of trip
        :param end: End location of trip
        :param mode: The mode of travel for the trip
        :param departure_time: Time of departure
        :param arrival_time: Time of arrival
        :return:
        """
        if departure_time is None and arrival_time is None:
            departure_time = datetime.now()
        self._dir_result = self._gmaps.directions(start, end, mode, departure_time=departure_time)[0]
