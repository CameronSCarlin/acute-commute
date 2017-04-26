import httplib
import requests

# Acute Commute
# Solving the first mile / last mile problem for travelers

# Authors:
# Connor Ameres (Beauty)
# Melanie Palmer (Boss)
# Will Young (Brain)
# Cameron Carlin (Brawn)

# use this server for prod, once it's on ec2
SERVER = 'ec2-34-200-220-123.compute-1.amazonaws.com'


def get_default():
    """
    Accesses landing page and prints raw html.

    :return: html string
    """
    h = httplib.HTTPConnection(SERVER)
    h.request('GET', 'http://' + SERVER + '/static/index.html')
    resp = h.getresponse()
    out = resp.read()
    return out


def get_api_info(form_dict):
    """
    form_dict can have keys 'start', 'end' and a key for each
    acceptable mode (walking, driving, transit, scooter, bicycling)
    if and only if that mode is to be considered. If a mode key
    is included the value should be 'on' (eg 'driving': 'on').
    Do not include mode as key if mode not to be used (eg do not
    do 'walking': 'off').

    :param form_dict: parameters for commute
    :return: JSON string
    """
    r = requests.post('http://' + SERVER + "/trip", data=form_dict)
    return r.text


if __name__ == '__main__':
    print "*" * 75
    print "test of my flask app running at ", SERVER
    print "created by Conner Ameres, Cameron Carlin, Melanie Palmer, and Will Young"
    print "*" * 75
    print " "
    print "******** html form for landing page **********"
    print get_default()
    print " "
    print "******** json output from commute query **********"
    form_dict = {'start': '101 Howard St. San francisco, CA',
                 'end': 'Fisherman\'s Wharf San Francisco CA',
                 'walking': 'on',
                 'driving': 'on'}
    print get_api_info(form_dict)
