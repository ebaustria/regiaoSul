import lib.coord_conversion as cc
import json


def message_json(local_coordinates: str, gps_coordinates: str, notification: str):
    dict_list = []

    message_timestamps = cc.timestamps_list(local_coordinates)
    message_gps = cc.gps_list(gps_coordinates)
    message_final_coords = cc.final_list(message_timestamps, message_gps)

    for name, gps, timestamp in message_final_coords:
        new_dict = {}
        new_dict["name"] = name
        new_dict["coordinates"] = gps
        new_dict["timestamp"] = timestamp
        new_dict["notification"] = notification

        dict_list.append(new_dict)

    notification = notification.split()

    file_name = notification[0] + "_" + notification[1] + ".json"
    json_file = json.dumps(dict_list, indent=2)

    with open(file_name, "w") as file:
        file.write(json_file)


def carried_messages(local_coordinates: str, gps_coordinates: str):
    dict_list = []

    carried_timestamps = cc.timestamps_list(local_coordinates)
    carried_gps = cc.gps_list(gps_coordinates)
    carried_final_coords = cc.final_list(carried_timestamps, carried_gps)

    for name, gps, timestamp, messages in carried_final_coords:
        new_dict = {}
        new_dict["name"] = name
        new_dict["coordinates"] = gps
        new_dict["timestamp"] = timestamp
        new_dict["messages"] = str(messages)

        dict_list.append(new_dict)

    json_file = json.dumps(dict_list, indent=2)

    with open("carried_messages.json", "w") as file:
        file.write(json_file)
