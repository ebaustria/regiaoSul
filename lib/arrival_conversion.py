import coord_conversion
import json


def make_arrivals(local_coordinates: str, gps_coordinates: str):
    dict_list = []

    arrivals_timestamps = coord_conversion.timestamps_list(local_coordinates)
    arrivals_gps = coord_conversion.gps_list(gps_coordinates)
    arrivals_final_coords = coord_conversion.final_list(arrivals_timestamps, arrivals_gps)

    for name, gps, timestamp in arrivals_final_coords:
        new_dict = {}
        new_dict["name"] = name
        new_dict["coordinates"] = gps
        new_dict["timestamp"] = timestamp
        new_dict["color"] = [253, 128, 93]

        dict_list.append(new_dict)

    json_file = json.dumps(dict_list, indent=2)

    with open("arrivals.json", "w") as file:
        file.write(json_file)
