from QueryParser import QueryParser


class Leg:
    """
    docstring for Leg
    """

    def __init__(self, query_parser, acceptable_modes):

        # assert query_parser.parse_num_segments() == 1, "Leg object can only have one segment"

        self._query_parser = query_parser
        self._acceptable_modes = acceptable_modes

        if len(acceptable_modes) > 1:
            self.find_best_mode()

        self._duration = self._query_parser.parse_duration()
        self._mode = self.get_mode()

    def find_best_mode(self):
        for mode in self._acceptable_modes:
            qp = QueryParser(self._query_parser.get_start(),
                             self._query_parser.get_end(),
                             mode,
                             self._query_parser.get_departure_time(),
                             self._query_parser.get_arrival_time())
            if qp.parse_duration() < self._query_parser.parse_duration():
                self.set_query_parser(qp)

    def get_duration(self):
        return self._duration

    def get_mode(self):
        return self._query_parser.parse_modes()

    def set_query_parser(self, query_parser):
        self._query_parser = query_parser

#
# # if transit is not a step, we want its mode and ending location (we know start already)
# if segment['travel_mode'] != 'TRANSIT':
#     self._steps.append({'lat_long': segment['end_location'], 'travel_mode': segment['travel_mode']})
# else:
#     self._steps.append({'lat_long': segment['end_location'],  # if transit, adds in agency and line
#                         'travel_mode': segment['travel_mode'],
#                         'agency': segment['transit_details']['line']['agencies'][0]['name'],
#                         'line': segment['transit_details']['line']['short_name']})