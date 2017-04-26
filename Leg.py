from __future__ import print_function

import re

lower = str.lower
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
        self._steps = []

        self._find_best_mode()
        self._build_directions()

    def _build_directions(self):
        d = {'start': self.get_start(), 'end': self.get_end(), 'duration': self.get_duration(),
             'mode': self.get_mode(), 'price_range': self.get_price_range(), 'steps': self.get_steps(),
             'start_location': self.get_start_location(), 'end_location': self.get_end_location()}
        self.set_directions(d)

    def _build_steps(self, query):
        def _step_builder(single_step):
            return {'start_location': single_step['start_location'],
                    'end_location': single_step['end_location'],
                    'duration': single_step['duration']['value'] / 60.0,
                    'mode': lower(single_step['travel_mode'])}
        steps = query.parse_segments()
        self._steps = [_step_builder(step) for step in steps]

    def _check_scooter(self):
        scooter_factor = 1.5
        qp = self.query_parse_factory('bicycling')
        if self._format_duration_as_minutes(qp.parse_duration()) * scooter_factor < self.get_duration():
            self._generate_stats_from_google(qp)
            self._mode = 'scooter'
            self._duration *= scooter_factor

    def _check_google(self, mode):
        qp = self.query_parse_factory(mode)
        if self._format_duration_as_minutes(qp.parse_duration()) < self.get_duration():
            self._generate_stats_from_google(qp)

    def _check_uber(self):
        try:
            start_lat, start_lon = self._start['lat'], self._start['lng']
            end_lat, end_lon = self._end['lat'], self._end['lng']
        except (KeyError, TypeError):
            print('using google for uber')
            qp = self.query_parse_factory('driving')
            start_dict = qp.parse_start_coordinate()
            end_dict = qp.parse_end_coordinate()
            start_lat, start_lon = start_dict['lat'], start_dict['lng']
            end_lat, end_lon = end_dict['lat'], end_dict['lng']

        uber_result = Uber_API.uber_estimate(start_lat, start_lon, end_lat, end_lon)

        if uber_result[2] < self._duration:
            self._generate_stats_from_uber(uber_result, start_lat, start_lon, end_lat, end_lon)

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
        self._distance = query.parse_distance()
        self._duration = self._format_duration_as_minutes(query.parse_duration())
        self.set_price_range((query.parse_cost(), query.parse_cost()))
        self._mode = lower(query.parse_modes()[0])
        self.set_start_loc_from_dict(query.parse_start_coordinate())
        self.set_end_loc_from_dict(query.parse_end_coordinate())
        self._build_steps(query)

    def _generate_stats_from_uber(self, query, start_lat, start_lon, end_lat, end_lon):
        self._distance = query[1]
        self._duration = query[2] / 60.0
        self.set_price_range((query[3], query[4]))
        self._mode = 'uber'
        self._steps = ['Hail Uber using Uber app',
                       'Patiently wait for driver',
                       'Glance at phone',
                       'Wait for driver',
                       'Plant wheat',
                       'Get in Uber',
                       'Speak to driver',
                       'Thank driver',
                       'Get out of Uber',
                       'Review ride']
        self.set_start_location(start_lat, start_lon)
        self.set_end_location(end_lat, end_lon)

    def get_mode(self):
        return self._mode

    def get_steps(self):
        return self._steps


def main():
    leg = Leg('101 Howard Stree San Francisco, CA', 'Fisherman\'s Wharf', ['walking'])
    print(leg.get_directions_json())

if __name__ == "__main__":
    main()
