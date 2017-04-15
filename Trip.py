from collections import defaultdict
from Leg import Leg
from string import lower
from QueryParser import QueryParser


class Trip:
    """docstring for Trip"""

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):

        self._acceptable_modes = acceptable_modes
        self._query_parser = QueryParser(start, end, acceptable_modes[0], departure_time=None, arrival_time=None)
        self._legs = defaultdict(Leg)
        self._build_legs()

    def _build_legs(self):
        # the end coordinates of the last stop are the start coordinates of the next segment
        for i, segment in enumerate(self._query_parser.parse_segments()):
            qp = QueryParser(segment['start_location'],
                             segment['end_location'],
                             lower(segment['travel_mode']),
                             self._query_parser.get_departure_time(),
                             self._query_parser.get_arrival_time())
            if segment['travel_mode'] == 'WALKING':
                self._legs[i] = Leg(qp, self._acceptable_modes)
            else:
                self._legs[i] = Leg(stqp, [segment['travel_mode']])

    def get_legs(self):
        return self._legs

    def set_query_parser(self, query_parser):
        self._query_parser = query_parser


def main():
    t = Trip("101 Howard Street San Francisco", "502 Cleveland St. Redwood City, CA", ["transit", 'bicycling', 'driving'])
    legs = t.get_legs()
    print legs
    for key in legs.keys():
        print legs[key]
        print legs[key].get_duration()
        print legs[key].get_mode()


if __name__ == "__main__":
    main()
