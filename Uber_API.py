
# coding: utf-8
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import keys


def uber_estimate(start_lat, start_long, end_lat, end_long):
    session = Session(server_token=keys.uber)
    client = UberRidesClient(session)
    response = client.get_products(start_lat, start_long)
    products = response.json.get('products')
    client = UberRidesClient(session)
    response_pickup = client.get_pickup_time_estimates(start_lat, start_long)
    estimate = client.get_price_estimates(
        start_latitude=start_lat,
        start_longitude=start_long,
        end_latitude=end_lat,
        end_longitude=end_long,
        seat_count=1
    ).json['prices'][0]
    # Uber Type, Distance (miles, float), Duration (seconds, float), low $, high $
    return (estimate['display_name'],
            estimate['distance'],
            estimate['duration']+response_pickup.json.get('times')[0]['estimate'],
            estimate['low_estimate'],
            estimate['high_estimate'])


def main():
    # Input: float start_lat, start_long, end_lat, end_long
    # Inputs
    start_latitude, start_longitude = 37.8081343, -122.4096086
    end_latitude, end_longitude = 37.7910977, -122.3928055
    seat_count = 1

    # Output: str Uber type, float distance, duration, low price, high price
    # (u'POOL', 1.77, 720, 3.0, 6.0)

    print uber_estimate(start_latitude, start_longitude, end_latitude, end_longitude)

if __name__ == "__main__":
    main()