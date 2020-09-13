from lib import coord_conversion
from lib import route_conversion
from lib import stop_conversion
from lib import arrival_conversion
from lib import message_conversion

print("Making trips JSON...")
coord_conversion.make_trips("local_coordinates.txt", "gps_coordinates.csv")

# print("Making routes JSON...")
# route_conversion.make_routes()

print("Making stops JSON...")
stop_conversion.make_stops("gps_coordinates.csv")

print("Making arrivals JSON...")
arrival_conversion.make_arrivals("arrivals.txt", "gps_coordinates.csv")

print("Making messages JSON...")
message_conversion.message_json("created_messages.txt", "gps_coordinates.csv", "creating message")
