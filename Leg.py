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
        """

        :param start (str or dict): Start location of trip
        :param end (str or dict): End location of trip
        :param mode (str): The mode of travel for the trip
        :param departure_time (str): Time of departure
        :param arrival_time (str): Time of arrival
        """
        PricedTrip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)
        self.set_duration(float('Inf'))
        self._mode = None
        self._steps = []

        self._find_best_mode()
        self._build_directions()

    def _build_directions(self):
        """
        Dictionary description of the Leg including start, end, steps, mode, etc. Used for
        JSON string.

        :return: None
        """
        d = {'start': self.get_start(), 'end': self.get_end(), 'duration': self.get_duration(),
             'mode': self.get_mode(), 'price_range': self.get_price_range(), 'steps': self.get_steps(),
             'start_location': self.get_start_location(), 'end_location': self.get_end_location()}
        self.set_directions(d)

    def _build_steps(self, query):
        """
        If the leg is divided into multiple steps (as is often the case with walking, bicycling, and
        driving trips), we convert the steps into standardized dictionary format having mode, start,
        end, etc for each step.

        :param query: QueryParser object
        :return: None
        """

        def _step_builder(single_step):
            return {'start_location': single_step['start_location'],
                    'end_location': single_step['end_location'],
                    'duration': single_step['duration']['value'] / 60.0,
                    'mode': lower(single_step['travel_mode'])}
        steps = query.parse_segments()
        self._steps = [_step_builder(step) for step in steps]

    def _check_scooter(self):
        """
        Instantiates a QueryParser with mode 'scooter' and checks if the duration of the QP is less than
        duration of self._duration (the fastest trip so far). If the scooter is the fastest
        trip, updates fields accordingly.

        :return: None
        """
        scooter_factor = 1.5
        qp = self.query_parse_factory('bicycling')
        if qp.parse_duration() * scooter_factor < self.get_duration():
            self._generate_stats_from_google(qp)
            self._mode = 'scooter'  # note we have to override bicycle manually
            self.set_duration(self.get_duration() * scooter_factor)  # also set duration by scalar factor

    def _check_google(self, mode):
        """
        Checks if mode is faster than fastest mode and updates fields as needed.

        :param mode:
        :return:
        """
        qp = self.query_parse_factory(mode)
        if qp.parse_duration() < self.get_duration():
            self._generate_stats_from_google(qp)

    def _check_uber(self):
        """
        Checks if Uber is faster than self._duration and updates fields accordingly.

        :return: None
        """
        try:
            start_lat, start_lon = self.get_start()['lat'], self.get_start()['lng']
            end_lat, end_lon = self.get_end()['lat'], self.get_end()['lng']
        except (KeyError, TypeError):
            # we have to use Google to get lat / lng if not given in original Leg
            # constructor call
            print 'using google for uber'
            qp = self.query_parse_factory('driving')
            start_dict = qp.parse_start_coordinate()
            end_dict = qp.parse_end_coordinate()
            start_lat, start_lon = start_dict['lat'], start_dict['lng']
            end_lat, end_lon = end_dict['lat'], end_dict['lng']

        uber_result = Uber_API.uber_estimate(start_lat, start_lon, end_lat, end_lon)

        if uber_result[2] < self.get_duration():
            self._generate_stats_from_uber(uber_result, start_lat, start_lon, end_lat, end_lon)

    def _find_best_mode(self):
        """
        Checks all acceptable modes for fastest mode.

        :return: None
        """
        for mode in self.get_acceptable_modes():
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

    def _generate_stats_from_google(self, query):
        """
        Updates all fields (trip info including duration, mode, etc) from a
        QueryParser object.

        :param query: QueryParser
        :return: None
        """
        self.set_distance(query.parse_distance())
        self.set_duration(query.parse_duration())
        self.set_price_range((query.parse_cost(), query.parse_cost()))
        self._mode = lower(query.parse_modes()[0])
        self.set_start_loc_from_dict(query.parse_start_coordinate())
        self.set_end_loc_from_dict(query.parse_end_coordinate())
        self._build_steps(query)

    def _generate_stats_from_uber(self, query, start_lat, start_lon, end_lat, end_lon):
        """
        Updates all fields (trip info including duration, mode, etc) from an Uber query.

        :param query: QueryParser
        :return: None
        """
        self._distance = query[1]
        self.set_duration(query[2] / 60.0)
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
    print leg.get_directions_json()

if __name__ == "__main__":
    main()
