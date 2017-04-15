from collections import defaultdict
from Leg import Leg
from string import lower
import re
from QueryParser import QueryParser


class Trip:
    """docstring for Trip"""

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):

        self._acceptable_modes = acceptable_modes
        self._query_parser = None
        self._duration = 0  # will be updated by set_query_parser
        self.set_query_parser(QueryParser(start, end, acceptable_modes[0], departure_time=None, arrival_time=None))
        if len(self._acceptable_modes) > 1:
            self._find_best_mode()
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
                self._legs[i] = Leg(qp, [segment['travel_mode']])

    def _find_best_mode(self):
        for mode in self._acceptable_modes:
            qp = QueryParser(self._query_parser.get_start(),
                             self._query_parser.get_end(),
                             mode,
                             self._query_parser.get_departure_time(),
                             self._query_parser.get_arrival_time())
            if self._format_duration_as_minutes(qp.parse_duration()) < self.get_duration_minutes():
                self.set_query_parser(qp)

    def _format_duration_as_minutes(self, duration_str):
        result = re.findall(pattern='\\d+', string=duration_str)
        if len(result) == 2:
            return 60.0 * int(result[0]) + int(result[1])
        return float(result[0])

    def get_duration_minutes(self):
        return self._duration

    def get_legs(self):
        return self._legs

    def set_query_parser(self, query_parser):
        self._query_parser = query_parser
        self._duration = self._format_duration_as_minutes(self._query_parser.parse_duration())


def main():
    t = Trip("101 Howard Street San Francisco", "502 Cleveland St. Redwood City, CA", ['transit', 'bicycling'])
    legs = t.get_legs()
    print legs
    print t.get_duration_minutes()
    print t._query_parser.parse_modes()
    for key in legs.keys():
        print legs[key]
        print legs[key].get_duration()
        print legs[key].get_mode()


if __name__ == "__main__":
    main()
