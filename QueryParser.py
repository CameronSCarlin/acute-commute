from QueryMaps import QueryMaps


class QueryParser(QueryMaps):
    """
    Provides methods for parsing the results of a Google Maps Query. Inherets
     QueryMaps
    """
    def __init__(self, start, end, mode, departure_time=None, arrival_time=None):
        """
        :param start (str or dict): Start location of trip
        :param end (str or dict): End location of trip
        :param mode (str): The mode of travel for the trip
        :param departure_time (str): Time of departure
        :param arrival_time (str): Time of arrival
        """
        QueryMaps.__init__(self, start, end, mode, departure_time, arrival_time)

        self._steps = []  # I don't think this is used

    def parse_cost(self):
        """
        Accesses price from QueryMaps result.

        :return: cost of trip in dollars
        """
        try:
            return self._dir_result['fare']['value']
        except KeyError:
            return 0

    def parse_distance(self):
        """
        Accesses distance of trip from QueryMaps result.

        :return: distance of trip in miles or feet
        """
        return self._dir_result['legs'][0]['distance']['text']

    def parse_duration(self):
        """
        Accesses duration of trip from QueryMaps result. Duration
        is represented as a string (e.g. 2 hr 5 min)

        :return: str representation of duration of trip
        """
        return self._dir_result['legs'][0]['duration']['value'] / 60.0

    def parse_modes(self):
        """
        Accesses the modes of travel for each segment in Google result.

        :return: list of modes for each segment (step) in the trip
        """
        return [segment['travel_mode'] for segment in self.parse_segments()]

    def parse_num_segments(self):
        """
        Accesses the number of segments in Google result.

        :return: number of segments in trip
        """
        return len(self.parse_segments())

    def parse_start_coordinate(self):
        """
        Accesses the start coordinate of Google result. Returns
         dictionary with keys ('lat' and 'lng').

        :return: dictionary of lat / lng start coordinates
        """
        return self._dir_result['legs'][0]['start_location']

    def parse_end_coordinate(self):
        """
        Accesses the end coordinate of Google result. Returns
         dictionary with keys ('lat' and 'lng').

        :return: dictionary of lat / lng end coordinates
        """
        return self._dir_result['legs'][0]['end_location']

    def parse_segments(self):
        """
        Accesses the segment descriptions of trip from Google.
        Segments are defined by Google.

        :return: Dictionary description of every segment of trip
        """
        return self._dir_result['legs'][0]['steps']


def main():
    pq = QueryParser('94597', '91354', 'bicycling')
    pq.print_directions()
    # print pq.parse_cost()
    # print pq.parse_distance()
    print pq.parse_duration()
    print len(pq.parse_segments())
    # print pq.parse_start_coordinate()

if __name__ == '__main__':
    main()
