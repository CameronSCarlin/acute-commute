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
        self._last_mile_modes = acceptable_modes  # acceptable modes for last leg of commute
        self.set_duration(0)
        self._transit_legs = []
        self._build_transit_legs()

    def _abridge_last_mile_modes(self, previous_mode):
        """
        Updates the modes allowed in the last leg based on previous_mode. This is called from
        _build_transit_legs when the leg currently being parsed is a transit leg.

        BUG: What if there is interem walking b/w transit stops?

        :param previous_mode:
        :return: None
        """
        last_mile_dict = {'uber': ['uber', 'walking', 'transit'], 'bicycling': ['bicycling', 'transit'],
                          'driving': ['uber', 'walking', 'transit'], 'walking': ['uber', 'walking', 'transit']}
        last_mile_modes = [mode for mode in last_mile_dict[previous_mode] if mode in self.get_acceptable_modes()]
        self._last_mile_modes = last_mile_modes

    def _append_leg(self, start, end, modes):
        """
        Adds a new leg to self._legs.

        :param start: the start location of the leg
        :param end: the end location of the leg
        :param modes: list of acceptable modes for leg
        :return: None
        """
        self._transit_legs.append(Leg(start,
                                      end,
                                      modes,
                                      self._departure_time,
                                      self._arrival_time))
        self._duration += self._transit_legs[-1].get_duration()

    def _build_transit_legs(self):
        """
        Builds self._legs by first instatiating a QueryParser  with 'transit' as only mode and
        setting self._query_parser to this instance. self._start and self._end locations are then
        set.

        The function then iterates over every segment in the transit trip. If the travel mode of
        the segment is walking (Google's default first/last mile mode), function appends a Leg
        object with all acceptable modes (Note the Leg objec searches for the best mode by default).
        Otherwise the segment will have mode transit and so we append a Leg that has start a transit
        station / stop and end at transit station / stop. If Leg added is a transit Leg, we update
        available last mile modes based on the best first mile mode.

        BUG: Best first mile mode not necessarily best last mile mode
        BUG: What if there there is interim walking between two transit modes
        FIX: Why not do if "transit" instead of if "walking". Much clearer.

        :return: None
        """
        self._original_query = QueryParser(self._start, self._end, 'transit', self._departure_time, self._arrival_time)
        self.set_start_loc_from_dict(self._original_query.parse_start_coordinate())
        self.set_end_loc_from_dict(self._original_query.parse_end_coordinate())
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
