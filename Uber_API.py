
# coding: utf-8

# In[3]:

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import keys


# In[18]:

# Inputs
start_latitude, start_longitude = 37.8081343, -122.4096086
end_latitude, end_longitude = 37.7910977, -122.3928055
seat_count = 1


# In[35]:

from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import keys

def uber_estimate(start_lat, start_long, end_lat, end_long):
    session = Session(server_token=keys.uber)
    client = UberRidesClient(session)
    response = client.get_products(start_latitude, start_longitude)
    products = response.json.get('products')
    product_id = products[0].get('product_id')
    estimate = client.get_price_estimates(
    start_latitude = start_latitude,
    start_longitude = start_longitude,
    end_latitude = end_latitude,
    end_longitude = end_longitude,
    seat_count = 1
    ).json['prices'][0]
    # Uber Type, Distance (miles, float), Duration (seconds, float), low $, high $
    return estimate['display_name'],estimate['distance'],estimate['duration'], estimate['low_estimate'], estimate['high_estimate']

# Input: float start_lat, start_long, end_lat, end_long
# Output: str Uber type, float distance, duration, low price, high price
print uber_estimate(start_latitude, start_longitude, end_latitude, end_longitude)

