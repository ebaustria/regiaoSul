# -*- coding: utf-8 -*-
from typing import List, Tuple, Set, Dict
from lib.project import Projector
import csv

WKT_BEGIN_LNSTR = 'LINESTRING ('
WKT_BEGIN_POINT = 'POINT ('
WKT_END = ')'
WKT_CRD_SEP = ' '
WKT_PNT_SEP = ', '
CSV_DELIMITER = ','
CSV_QUOTECHAR = '"'
# what the hack is a fallback duration?
FALLBACK_DURATION = 3


def write_wkt_linestring(coords: List[Tuple[float, float]], file: str, append=False) -> None:
    content = ''
    if append:
        content += '\n\n'
    content += WKT_BEGIN_LNSTR

    for i, c in enumerate(coords):
        content += str(c[0]) + WKT_CRD_SEP + str(c[1])
        if i < len(coords) - 1:
            content += WKT_PNT_SEP

    content += WKT_END

    with open(file, 'a+' if append else 'w+') as fp:
        fp.write(content)


def write_wkt_points(coords: Set[Tuple[float, float]], file: str, append=False):
    content = ''
    if append:
        content += '\n\n'

    for i, c in enumerate(coords):
        content += WKT_BEGIN_POINT
        content += str(c[0]) + WKT_CRD_SEP + str(c[1])
        content += WKT_END
        if i < len(coords) - 1:
            content += '\n\n'

    with open(file, 'a+' if append else 'w+') as fp:
        fp.write(content)


def write_csv_stops(coords: List[Tuple[float, float]], durations: List[int], file: str):
    with open(file, 'w+') as fp:
        w = csv.writer(fp,
                       delimiter=CSV_DELIMITER,
                       quotechar=CSV_QUOTECHAR,
                       quoting=csv.QUOTE_MINIMAL)
        if not durations:
            durations = len(coords) * [FALLBACK_DURATION]
        for i, duration in enumerate(durations):
            c = coords[i]
            # write duration in seconds
            duration_s = 30
            if duration > 0:
                duration_s = duration * 60
            w.writerow([
                '{} {}'.format(c[0], c[1]),
                duration_s
            ])


def write_csv_schedule(schedule: List, file: str):
    with open(file, 'w+') as fp:
        w = csv.writer(fp,
                       delimiter=CSV_DELIMITER,
                       quotechar=CSV_QUOTECHAR,
                       quoting=csv.QUOTE_MINIMAL)
        w.writerows(schedule or [])


def write_local_and_gps(proj: Projector, routes: Dict) -> None:
    main_local_to_gps = set()

    for route_name in routes.keys():
        nodes = routes[route_name]['nodes']
        stops = routes[route_name]['stops']

        for key, value in sorted(proj.local_to_gps.items()):
            if value in nodes or value in stops:
                main_local_to_gps.add((key, value))

    with open('gps_coordinates_brazil.csv', 'w') as f:
        writer = csv.writer(f)
        for local, gps in sorted(main_local_to_gps):
            writer.writerow([local, gps])
