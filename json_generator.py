from lib import coord_conversion
from lib import route_conversion
from lib import stop_conversion
from lib import arrival_conversion
from lib import message_conversion
import sys

local_coords = sys.argv[1]
gps_coords = sys.argv[2]
arrivals = sys.argv[3]
messages = sys.argv[4]

print("Making trips JSON...")
coord_conversion.make_trips(local_coords, gps_coords)

print("Making routes JSON...")
route_conversion.make_routes(gps_coords)

print("Making stops JSON...")
stop_conversion.make_stops(gps_coords)

print("Making arrivals JSON...")
arrival_conversion.make_arrivals(arrivals, gps_coords)

print("Making messages JSON...")
message_conversion.message_json(messages, gps_coords)

# print("Making carried messages JSON...")
# message_conversion.carried_messages("carried_messages.txt", "gps_coordinates_brazil.csv")
