from Leg import Leg
from TransitTrip import TransitTrip
from PricedTrip import PricedTrip
from QueryParser import QueryParser


class Commute(PricedTrip):
    """
    docstring for Trip
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        PricedTrip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)
        self._queries_dict = {'transit': None, 'driving': None, 'walking': None,
                              'scooter': None, 'bicycling': None, 'uber': None}

        self.set_duration(0.0)
        self._primary_mode = None

        self._create_original_queries()
        self._choose_best_trip()

    def _choose_best_trip(self):
        times = [(key, self._queries_dict[key].get_duration()) for key in self._queries_dict.keys()
                 if self._queries_dict[key] is not None]
        self._primary_mode = min(times, key=lambda tup: tup[1])[0]
        self._generate_best_stats()

    def _create_original_queries(self):
        for key in self._queries_dict.keys():
            if key in self.get_acceptable_modes():
                if key == 'transit':
                    self._queries_dict[key] = self._transit_trip_factory(key)
                else:
                    self._queries_dict[key] = self._leg_factory(key)

    def _generate_best_stats(self):
        best_trip = self._queries_dict[self._primary_mode]
        self._duration = best_trip.get_duration()
        self._distance = best_trip.get_distance()
        self._price_range = best_trip.get_price_range()
        self._directions = best_trip.get_directions()

    def get_primary_mode(self):
        return self._primary_mode

    def get_primary_trip_object(self):
        if self._primary_mode is None:
            print "Mode not set"
            return None
        return self._queries_dict[self._primary_mode]

    def _leg_factory(self, mode):
        return Leg(self._start, self._end, mode, self._departure_time, self._arrival_time)

    def _transit_trip_factory(self, mode):
        return TransitTrip(self._start, self._end, mode, self._departure_time, self._arrival_time)

    def _query_parse_factory(self, mode):
        return QueryParser(self._start, self._end, mode, self._departure_time, self._arrival_time)


def main():
    t = Commute("101 Howard Street San Francisco", "502 Cleveland St. Redwood City, CA", ['transit'])
    print "Trip details:"
    print "Primary mode: %s" % t.get_primary_mode()
    if t.get_primary_mode() == 'transit':
        print "----------- Legs ------------"
        t.get_primary_trip_object().print_transit_legs()
        print "-" * 25
    print "Duration: %s minutes" % t.get_duration()


if __name__ == "__main__":
    main()
