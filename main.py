#!/usr/bin/env python
import datetime as dt
from shapely.geometry import Polygon
from fastkml import kml
from glob import glob


class SearchPosition:
    def __init__(self, geometry, date):
        self.geometry = geometry
        self.date = date

    def __str__(self):
        return f'SearchPosition({self.date}, {self.geometry})'


def get_usr_request():
    #area = LinearRing(
    #    [(55.58734, -72.26807, 0), (47.12514, -67.57458, 0), (38.84882, -59.56221, 0), (45.44252, -58.01071, 0),
    #     (55.15113, -65.58617, 0), (64.48255, -69.85429, 0), (55.58734, -72.26807, 0)])
    #return SearchPosition(area, dt.date(2021, 4, 27))
    area = Polygon([(-42.49884, 49.153282), (-41.985996, 50.785885), (-45.565868, 51.181957), (-45.959145, 49.54763), (-42.49884, 49.153282)])
    return SearchPosition(area, dt.datetime(2021, 5, 10, 9))


def get_positions_from_kml(kml_path):
    """Read kml file with Acquisition Segments"""
    print(f'Reading {kml_path}')
    k = kml.KML()
    with open(kml_path, 'r') as f:
        kml_s = f.read()
    k.from_string(kml_s.encode('utf-8'))
    return get_positions(k)


def get_positions(elem):
    """Find all positions in kml structure"""
    if isinstance(elem, kml.Placemark):
        return [SearchPosition(elem.geometry, elem.begin)]
    else:
        positions = list()
        for feature in elem.features():
            positions.extend(get_positions(feature))
        return positions


def is_matching(request, position):
    if (request.geometry.intersects(position.geometry) and
            request.date.month == position.date.month and
            request.date.day == position.date.day and
            request.date.hour == position.date.hour):
        return True


def main():
    request = get_usr_request()

    #kml_path = '../Sentinel-1A_MP_20210427T160000_20210517T180000.kml'
    #kml_path = '../Sentinel-1B_MP_20210528T160000_20210617T180000.kml'

    for kml_path in glob('./acquisition_segments/Sentinel-1B*.kml'):
        available = get_positions_from_kml(kml_path)

        for position in available:
            if is_matching(request, position):
                print(f'Match: {position}')


if __name__ == '__main__':
    main()
