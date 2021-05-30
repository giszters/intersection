#!/usr/bin/env python
import xml.etree.ElementTree as ET
import datetime as dt
from shapely.geometry import Polygon


class SearchPosition:
    """SearchPosition is Polygon with date."""
    def __init__(self, area, date):
        self.polygon = area
        self.date = date

    def __str__(self):
        return f'SearchPosition({self.date}, {self.polygon})'


def get_usr_request():
    area = str2polygon('55.58734,-72.26807,0 47.12514,-67.57458,0 38.84882,-59.56221,0 45.44252,-58.01071,0 55.15113,-65.58617,0 64.48255,-69.85429,0 55.58734,-72.26807,0')
    return SearchPosition(area, None)


def placemark2position(pmark):
    tspan = pmark.findall('.//{http://www.opengis.net/kml/2.2}name')
    if len(tspan) != 1:
        raise Exception('Too many names')
    date_valid = dt.datetime.strptime(tspan[0].text, '%Y-%m-%dT%H:%M:%S')

    lring = pmark.findall('.//{http://www.opengis.net/kml/2.2}LinearRing')
    if len(lring) != 1:
        raise Exception('Too many LinearRings')
    coords = lring[0].find('.//{http://www.opengis.net/kml/2.2}coordinates').text

    return SearchPosition(str2polygon(coords), date_valid)


def str2point(position_s):
    lon, lat, z = position_s.split(',')
    if z != '0':
        raise Exception(f'Were above the ground at level {z}!')
    return float(lon), float(lat)


def str2polygon(coord_s):
    points_s = coord_s.split(' ')
    points = list()
    for point_s in points_s:
        points.append(str2point(point_s))
    return Polygon(points)


def get_positions_from_kml(kml_path):
    kml = ET.parse(kml_path)
    root = kml.getroot()
    pmarks = list()
    for pmark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        pmarks.append(placemark2position(pmark))
    return pmarks


def is_matching(request, position):
    #if request.area.intersects(position.area) and request.date == position.date:
    if request.polygon.intersects(position.polygon):
        return True


def main():
    request = get_usr_request()

    kml_path = "../Sentinel-1A_MP_20210427T160000_20210517T180000.kml"
    available = get_positions_from_kml(kml_path)

    for position in available:
        if is_matching(request, position):
            print('Got one!')


if __name__ == '__main__':
    main()
