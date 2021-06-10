import boto3
import datetime as dt
import json
from shapely.geometry import Polygon


BUCKET = 'sentinel-s1-l1c'

## search segments of given type
PRODUCT_TYPE = 'GRD'
MODE = 'IW'
POLARIZATION = 'DH'


def download_file(file):
    s3 = boto3.client('s3')
    f = s3.get_object(Bucket=BUCKET, Key=file, RequestPayer='requester')
    return f['Body'].read()


def get_geometry_from_product_info(pinfo_json):
    data = json.loads(pinfo_json)
    coords = data['footprint']['coordinates'][0][0]
    return Polygon(coords)


def get_available_metadata(date):
    """Return metadata of available segments for given date."""
    s3 = boto3.client('s3')
    prefix = f'{PRODUCT_TYPE}/{date.year}/{date.month}/{date.day}/{MODE}/{POLARIZATION}'
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix, RequestPayer='requester')
    ## select only productInfo.json files
    return [i for i in response['Contents'] if 'productInfo.json' in i['Key']]


def test():
    date = dt.datetime(2021, 5, 10)

    pinfos = get_available_metadata(date)
    for pinfo in pinfos:
        print(pinfo)

    if pinfos:
        content = download_file(pinfos[0]['Key'])
        print(content)
        geometry = get_geometry_from_product_info(content)
        print(geometry)


if __name__ == '__main__':
    test()