class Trip:
    """
    Base class for QueryMaps and PricedTrip. Simply defines fields and methods used by those
    classes and subclasses of those classes.
    """

    def __init__(self, start, end, acceptable_modes, departure_time=None, arrival_time=None):
        """

        :param start (str or dict): Start location of trip
        :param end (str or dict): End location of trip
        :param mode (str): The mode of travel for the trip
        :param departure_time (str): Time of departure
        :param arrival_time (str): Time of arrival
        """
        if type(acceptable_modes) is list:
            self._acceptable_modes = acceptable_modes
        elif type(acceptable_modes) is tuple:
            self._acceptable_modes = [mode for mode in acceptable_modes]
        elif type(acceptable_modes) is str:
            self._acceptable_modes = [acceptable_modes]
        else:
            assert False, "acceptable_modes shold be list, tuple, or string. Got %s" % type(acceptable_modes)

        assert isinstance(start, (str, dict)), "start should be str or dict got %s" % type(start)
        assert isinstance(end, (str, dict)), "start should be str or dict got %s" % type(end)
        if departure_time is not None:
            assert isinstance(departure_time, str), "departure_time should be str. Got %s" % type(departure_time)
        if arrival_time is not None:
            assert isinstance(arrival_time, str), "arrival_time should be str. Got %s" % type(arrival_time)

        self._start = start
        self._end = end
        self._departure_time = departure_time
        self._arrival_time = arrival_time

    def get_acceptable_modes(self):
        return self._acceptable_modes

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_departure_time(self):
        return self._departure_time

    def get_arrival_time(self):
        return self._arrival_time
