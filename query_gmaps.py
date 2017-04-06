from datetime import datetime
import googlemaps
import keys
import pprint

def initial_directions(start, end, mode, departure_time=datetime.now()):
    dir_result = gmaps.directions(start,
        end,
        mode,
        departure_time=departure_time)[0]
    #pp = pprint.PrettyPrinter(indent=4)                                    # uncomment if you want pretty print
    #pp.pprint(dir_result)
    init_cost = dir_result['fare']['value']                                 # in dollars
    init_distance = dir_result['legs'][0]['distance']['text']               # miles or feet
    init_duration = dir_result['legs'][0]['duration']['text']               # time
    start_coordinate = dir_result['legs'][0]['start_location']
    steps = []                                                              # will be list of the form of transportation and the ending coordinates of that transit
    for segment in dir_result['legs'][0]['steps']:                          # the end coordinates of the last stop are the start coordinates of the next segment
        if segment['travel_mode'] != 'TRANSIT':                             # if transit is not a step, we want its mode and ending location (we know start already)
            steps.append({'lat_long' : segment['end_location'],
                          'travel_mode' : segment['travel_mode']})
        else:
            steps.append({'lat_long' : segment['end_location'],             # if transit, adds in agency and line
                          'travel_mode' : segment['travel_mode'],
                          'agency': segment['transit_details']['line']['agencies'][0]['name'],
                          'line' : segment['transit_details']['line']['short_name']})
    return init_cost, init_distance, init_duration, start_coordinate, steps


if __name__ == '__main__':
    gmaps = googlemaps.Client(keys.gmaps)
    now = datetime.now()
    print initial_directions("101 Howard Street San Francisco",
        "Fisherman's Wharf",
        "transit",
        now)