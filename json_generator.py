from lib import coord_conversion
from lib import route_conversion
from lib import stop_conversion
from lib import arrival_conversion
from lib import message_conversion

print("Making trips JSON...")
coord_conversion.make_trips("local_coordinates_brazil.txt", "gps_coordinates_brazil.csv")

print("Making routes JSON...")
route_conversion.make_routes("gps_coordinates_brazil.csv")

print("Making stops JSON...")
stop_conversion.make_stops("gps_coordinates_brazil.csv")

print("Making arrivals JSON...")
arrival_conversion.make_arrivals("arrivals.txt", "gps_coordinates_brazil.csv")

print("Making messages JSON...")
message_conversion.message_json("messages_brazil.txt", "gps_coordinates_brazil.csv")

# print("Making carried messages JSON...")
# message_conversion.carried_messages("carried_messages.txt", "gps_coordinates_brazil.csv")
