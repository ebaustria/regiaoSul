from typing import List, Dict
import json
import wkt_parser
import coord_conversion


def build_list(stations: List[List[float]]) -> List[Dict]:
    json_list = []
    for coord in stations:
        new_station = {
            "name": "stop name",
            "coordinates": coord
        }
        json_list.append(new_station)

    return json_list


def make_stops(gps_coordinates: str) -> None:

    stops = []
    coords_list = coord_conversion.gps_list(gps_coordinates)

    with open("stations.wkt", 'r') as stations:
        stations = stations.readlines()
        stations = wkt_parser.parse_wkt_stops(stations)

    for local, gps in coords_list:
        for station in stations:
            if local[0] == station[0] and local[1] == station[1]:
                stops.append(gps)

    result = build_list(stops)

    stops_json = json.dumps(result, indent=2)

    with open("stops.json", "w") as file:
        file.write(stops_json)
