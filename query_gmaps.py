from datetime import datetime

import googlemaps

import keys

if __name__ == '__main__':
    gmaps = googlemaps.Client(keys.gmaps)
    now = datetime.now()
    directions_result = gmaps.directions("101 Howard Street San Francisco",
        "Fisherman's Wharf",
        mode="transit",
        departure_time=now)
