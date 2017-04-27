from Leg import Leg
from TransitTrip import TransitTrip
from PricedTrip import PricedTrip


class Commute(PricedTrip):
    """
    Class to actually interface with for performing searches.
    """
    available_modes = ['transit', 'driving', 'walking', 'scooter', 'bicycling', 'uber']

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        PricedTrip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)

        self._trips_dict = {mode: None for mode in Commute.available_modes}
        self._primary_mode = None
        self._best_trip = None
        self._legs = []

        self.set_duration(0.0)
        self._create_original_queries()
        self._choose_best_trip()
        self._generate_best_stats()

    def _build_directions(self):
        """
        Creates and fills self._dictionary, which is a dictionary representation of the commute.

        :return: None
        """
        d = {'start': self.get_start(), 'end': self.get_end(), 'duration': self.get_duration(),
             'mode': self.get_primary_mode(), 'price_range': self.get_price_range(), 'legs': self.get_legs(),
             'start_location': self.get_start_location(), 'end_location': self.get_end_location()}
        self.set_directions(d)

    def _build_legs(self):
        """
        Fills the legs of this commute.

        :return: None
        """
        if self._primary_mode == 'transit':
            for transit_leg in self._best_trip.get_transit_legs():
                self._legs.append(transit_leg.get_directions())
        else:
            self._legs.append(self._best_trip.get_directions())

    def _choose_best_trip(self):
        """
        Commute first creates the best trip for each of the acceptable modes. This function
        chooses the fastest Commute option and sets self._primary mode accordingly.

        :return: None
        """
        times = [(key, self._trips_dict[key].get_duration()) for key in self._trips_dict.keys()
                 if self._trips_dict[key] is not None]
        self._primary_mode = min(times, key=lambda tup: tup[1])[0]

    def _create_original_queries(self):
        """
        Performs queries for all acceptable modes and stores in self._trips_dict

        :return: None
        """
        for key in self._trips_dict.keys():
            if key in self.get_acceptable_modes():
                if key == 'transit':
                    self._trips_dict[key] = self._transit_trip_factory()
                else:
                    self._trips_dict[key] = self._leg_factory(key)

    def _generate_best_stats(self):
        """
        Once the best mode (best commute / query) has been determined, this function
        is called to fill all information for this commute.

        :return: None
        """
        self._best_trip = self._trips_dict[self._primary_mode]
        self._duration = self._best_trip.get_duration()
        self._distance = self._best_trip.get_distance()
        self._price_range = self._best_trip.get_price_range()
        self.set_start_loc_from_dict(self._best_trip.get_start_location())
        self.set_end_loc_from_dict(self._best_trip.get_end_location())
        self._build_legs()
        self._build_directions()

    def get_legs(self):
        return self._legs

    def get_primary_mode(self):
        return self._primary_mode

    def get_primary_trip_object(self):
        if self._primary_mode is None:
            print "Mode not set"
            return None
        return self._trips_dict[self._primary_mode]

    def _leg_factory(self, mode):
        return Leg(self._start, self._end, mode, self._departure_time, self._arrival_time)

    def _transit_trip_factory(self):
        return TransitTrip(self._start, self._end, self.get_acceptable_modes(), self._departure_time, self._arrival_time)


def main():
    t = Commute('101 Howard Street San Francisco', 'Broadway Plaza, Walnut Creek, CA', ['bicycling', 'transit'])
    print "Trip details:"
    print "Primary mode: %s" % t.get_primary_mode()
    if t.get_primary_mode() == 'transit':
        print "----------- Legs ------------"
        t.get_primary_trip_object().print_transit_legs()
        print "-" * 25
    print "Duration: %s minutes" % t.get_duration()
    print t.get_directions_json()

if __name__ == "__main__":
    main()
