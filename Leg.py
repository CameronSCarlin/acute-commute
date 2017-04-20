from QueryParser import QueryParser
import re
from string import lower
from PricedTrip import PricedTrip
import Uber_API


class Leg(PricedTrip):
    """
    I think we are defining a leg as a trip using only one mode of transportation, but
    we don't have a way to enforce it.
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        PricedTrip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)

        self.set_duration(float('Inf'))
        self._mode = None

        self._find_best_mode()

    def _check_scooter(self):
        qp = self._quick_parse('bicycling')
        if self._format_duration_as_minutes(qp.parse_duration()) < self.get_duration():
            self._generate_stats_from_google(qp)

        self._mode = 'scooter'
        self._duration *= 1.5

    def _check_google(self, mode):

        qp = self._quick_parse(mode)
        if self._format_duration_as_minutes(qp.parse_duration()) < self.get_duration():
            self._generate_stats_from_google(qp)

    def _check_uber(self):
        try:
            start_lat, start_lon = self._start['lat'], self._start['lng']
            end_lat, end_lon = self._end['lat'], self._end['lng']
        except (KeyError, TypeError):
            print 'using google for uber'
            qp = self._quick_parse('driving')
            start_dict = qp.parse_start_coordinate()
            end_dict = qp.parse_end_coordinate()
            start_lat, start_lon = start_dict['lat'], start_dict['lng']
            end_lat, end_lon = end_dict['lat'], end_dict['lng']

        uber_result = Uber_API.uber_estimate(start_lat, start_lon, end_lat, end_lon)

        if uber_result[2] < self._duration:
            self._generate_stats_from_uber(uber_result)

    def _find_best_mode(self):
        for mode in self._acceptable_modes:
            if mode == 'uber':
                self._check_uber()
            elif mode == 'lyft':
                assert False, "We do not currently support Lyft. Sorry."
            elif mode in ['driving', 'bicycling', 'walking', 'transit']:
                self._check_google(mode)
            elif mode == 'scooter':
                self._check_scooter()
            else:
                assert False, 'No good mode given: %s given' % mode

    def _format_duration_as_minutes(self, duration_str):
        result = re.findall(pattern='\\d+', string=duration_str)
        if len(result) == 2:
            return 60.0 * int(result[0]) + int(result[1])
        return float(result[0])

    def _generate_stats_from_google(self, query):
        self._directions = query.get_directions_result()
        self._distance = query.parse_distance()
        self._duration = self._format_duration_as_minutes(query.parse_duration())
        self._price_range = query.parse_cost()
        self._mode = lower(query.parse_modes()[0])

    def _generate_stats_from_uber(self, query):
        self._directions = query[0]
        self._distance = query[1]
        self._duration = query[2] / 60.0
        self._price_range = [query[3], query[4]]
        self._mode = 'uber'

    def get_mode(self):
        return self._mode

    def _quick_parse(self, mode):
        return QueryParser(self._start, self._end, mode, self._departure_time, self._arrival_time)
