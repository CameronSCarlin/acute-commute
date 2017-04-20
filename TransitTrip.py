from Leg import Leg
from PricedTrip import PricedTrip
from QueryParser import QueryParser
from string import lower


class TransitTrip(PricedTrip):
    """
    docstring for TransitTrip
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        PricedTrip.__init__(self, start, end, acceptable_modes, departure_time, arrival_time)
        self._last_mile_modes = acceptable_modes
        self.set_duration(0)
        self._transit_legs = []
        self._build_transit_legs()

    def _abridge_last_mile_modes(self, previous_mode):
        last_mile_dict = {'uber': ['uber', 'walking'], 'bicycling': ['bicycling'],
                          'driving': ['uber', 'walking'], 'walking': ['uber', 'walking']}
        self._last_mile_modes = last_mile_dict[previous_mode]

    def _append_leg(self, start, end, modes):
        self._transit_legs.append(Leg(start,
                                      end,
                                      modes,
                                      self._departure_time,
                                      self._arrival_time))
        self._duration += self._transit_legs[-1].get_duration()

    def _build_transit_legs(self):
        self._original_query = QueryParser(self._start, self._end, 'transit', self._departure_time, self._arrival_time)
        modes_abridged = False
        for segment in self._original_query.parse_segments():
            if segment['travel_mode'] == 'WALKING':
                temp_modes = self._last_mile_modes
            else:
                temp_modes = [lower(segment['travel_mode'])]

            self._append_leg(segment['start_location'], segment['end_location'], temp_modes)

            if not modes_abridged and self._transit_legs[-1].get_mode() == 'transit':
                try:
                    self._abridge_last_mile_modes(self._transit_legs[-2].get_mode())
                    modes_abridged = True
                except IndexError:
                    print "transit was first leg"

    def get_transit_legs(self):
        return self._transit_legs

    def print_transit_legs(self):
        for leg in self._transit_legs:
            print "Mode: %s\nDuration: %s\n" % (leg.get_mode(), leg.get_duration())
