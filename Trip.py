from collections import defaultdict
from Leg import Leg
from string import lower
from QueryParser import QueryParser


class Trip:
    """docstring for Trip"""

    def __init__(self, query_parser, acceptable_modes):

        self._query_parser = query_parser

        # {'walk': True, 'drive': True, 'bike': True, 'skate': False, 'ride': True}
        self._acceptable_modes = acceptable_modes

        self._legs = defaultdict(Leg)
        self._build_legs()

    def _build_legs(self):
        # the end coordinates of the last stop are the start coordinates of the next segment
        for i, segment in enumerate(self._query_parser.parse_segments()):
            if segment['travel_mode'] == 'WALKING':
                qp = QueryParser(self._query_parser.get_start(),
                                 self._query_parser.get_end(),
                                 'walking',
                                 self._query_parser.get_departure_time(),
                                 self._query_parser.get_arrival_time())
                self._legs[i] = Leg(qp, self._acceptable_modes)
            else:
                qp = QueryParser(self._query_parser.get_start(),
                                 self._query_parser.get_end(),
                                 lower(segment['travel_mode']),
                                 self._query_parser.get_departure_time(),
                                 self._query_parser.get_arrival_time())
                self._legs[i] = Leg(qp, [segment['travel_mode']])

    def get_legs(self):
        return self._legs


def main():
    qp = QueryParser("101 Howard Street San Francisco", "Fisherman's Wharf", "transit")
    t = Trip(qp, ['driving', 'bicycling'])
    legs = t.get_legs()
    print legs
    print legs[0].get_duration()
    print legs[0].get_mode()

if __name__ == "__main__":
    main()
