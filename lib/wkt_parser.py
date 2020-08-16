from typing import List


def parse_wkt_route(nodes) -> List[List[float]]:
    list_to_build = []
    nodes = nodes.strip("LINESTRING ()")
    nodes = nodes.split(',')

    for node in nodes:
        node = node.split()
        node[0] = float(node[0])
        node[1] = float(node[1])
        new_node = [node[1], node[0]]
        list_to_build.append(new_node)

    return list_to_build


def parse_wkt_stops(stops: List[str]) -> List[List[float]]:
    result = []

    for row in stops:
        row = row.strip("POINT (")
        row = row.split()
        row[1] = row[1].strip(')')
        row[0] = float(row[0])
        row[1] = float(row[1])
        result.append(row)

    return result
