#!/usr/bin/env python
import datetime as dt
from shapely.geometry import LinearRing
from fastkml import kml


class SearchPosition:
    """SearchPosition is Polygon with date."""

    def __init__(self, geometry, date):
        self.geometry = geometry
        self.date = date

    def __str__(self):
        return f'SearchPosition({self.date}, {self.geometry})'


def get_usr_request():
    area = LinearRing(
        [(55.58734, -72.26807, 0), (47.12514, -67.57458, 0), (38.84882, -59.56221, 0), (45.44252, -58.01071, 0),
         (55.15113, -65.58617, 0), (64.48255, -69.85429, 0), (55.58734, -72.26807, 0)])
    return SearchPosition(area, dt.date(2021, 4, 27))


def get_positions_from_kml(kml_path):
    """Read kml file with Acquisition Segments"""
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
        ft = list()
        for feat in elem.features():
            ft.extend(get_positions(feat))
        return ft


def is_matching(request, position):
    if (request.geometry.intersects(position.geometry) and
            request.date.year == position.date.year and
            request.date.month == position.date.month and
            request.date.day == position.date.day):
        return True


def main():
    request = get_usr_request()

    kml_path = '../Sentinel-1A_MP_20210427T160000_20210517T180000.kml'
    available = get_positions_from_kml(kml_path)

    for position in available:
        if is_matching(request, position):
            print(f'Match: {position}')


if __name__ == '__main__':
    main()
