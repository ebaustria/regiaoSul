from typing import Tuple, List
import lib.coord_conversion as cc
import json


def make_arrivals(local_coordinates: str, gps_coordinates: str):
    # dict_list = []

    arrivals_timestamps = cc.timestamps_list(local_coordinates)
    arrivals_gps = cc.gps_list(gps_coordinates)
    arrivals_final_coords = cc.final_list(arrivals_timestamps, arrivals_gps)

    dict_list = [single_dictionary(entry) for entry in arrivals_final_coords]

    json_file = json.dumps(dict_list, indent=2)

    with open("arrivals.json", "w") as file:
        file.write(json_file)


def single_dictionary(tup: Tuple[str, List[float], float, int]):
    new_dict = {}
    new_dict["name"] = tup[0]
    new_dict["coordinates"] = tup[1]
    new_dict["timestamp"] = tup[2]
    new_dict["color"] = [253, 128, 93]

    return new_dict
