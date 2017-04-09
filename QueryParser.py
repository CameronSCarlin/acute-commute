from QueryMaps import QueryMaps


class QueryParser(QueryMaps):
    """
    ParseQuery
    """
    def __init__(self, start, end, mode, departure_time=None, arrival_time=None):
        QueryMaps.__init__(self, start, end, mode, departure_time, arrival_time)
        self._steps = []

    def parse_cost(self):
        return self._dir_result['fare']['value']

    def parse_distance(self):
        """
        Could be miles or feet
        :return:
        """
        return self._dir_result['legs'][0]['distance']['text']

    def parse_duration(self):
        """
        :return:
        """
        return self._dir_result['legs'][0]['duration']['text']

    def parse_modes(self):
        return [segment['travel_mode'] for segment in self.parse_segments()]

    def parse_num_segments(self):
        return len(self.parse_segments())

    def parse_start_coordinate(self):
        """
        :return:
        """
        return self._dir_result['legs'][0]['start_location']

    def parse_segments(self):
        return self._dir_result['legs'][0]['steps']


def main():
    pq = QueryParser("101 Howard Street San Francisco", "Fisherman's Wharf", "transit")
    pq.print_directions()
    # print pq.parse_cost()
    # print pq.parse_distance()
    # print pq.parse_duration()
    print len(pq.parse_segments())
    # print pq.parse_start_coordinate()

if __name__ == '__main__':
    main()

