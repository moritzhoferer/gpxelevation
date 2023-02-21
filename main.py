#! ./venv/bin/python3

import requests
import gpxpy
import gpxpy.gpx
import srtm


elevation_data = srtm.get_data()

wgs84_to_lv95 = 'http://geodesy.geo.admin.ch/reframe/wgs84tolv95?easting={lon:f}&northing={lat:f}&format=json'
swisstopo_elevation = 'https://api3.geo.admin.ch/rest/services/height?easting={easting}&northing={northing}&sr=2056'


def transform_wgs84_to_lv95(longitude, latitude, mode='api') -> dict:
    """Transform WGS84 coordinates to LV95"""
    if mode == 'api':
        re = requests.get(
            wgs84_to_lv95.format(lon=longitude, lat=latitude)
        )
        _dict = re.json()
    elif mode == 'approx':
        # Source: https://www.swisstopo.admin.ch/de/karten-daten-online/calculation-services.html
        _dict = {}
        _phi = (float(latitude) * 3600. - 169028.66) / 1e4
        _lambda = (float(longitude) * 3600. - 26782.5) / 1e4
        _dict['easting'] = 2600072.37 + 211455.93 * _lambda - 10938.51  * _lambda * _phi \
            - 0.36 * _lambda * _phi**2  - 44.54 * _lambda**3
        _dict['northing'] = 1200147.07 + 308807.95 * _phi + 3745.25 * _lambda**2 + 76.63 * _phi**2 \
            - 194.56 * _lambda**2 * _phi + 119.79 * _phi**3
    else:
        raise NotImplementedError('You are calling a not-implemented mode.')
    return _dict


def get_swisstopo_polyline_request(gpx: gpxpy.gpx.GPX) -> str:
    _coords = ''
    _points = 0
    for point in gpx.walk(only_points=True):
        _coordinates = transform_wgs84_to_lv95(point.longitude, point.latitude)
        _points += 1
        _coords += f"[{_coordinates['easting']}%2C{_coordinates['northing']}]%2C"
    return 'https://api3.geo.admin.ch/rest/services/profile.json?'\
        + f'geom={{%22type%22%3A%22LineString%22%2C%22coordinates%22%3A[{_coords[:-3]}]}}' \
        + f'&distinct_points=TRUE&nb_points={_points}'

def get_swisstopo_elevation(longitude, latitude) -> str:
    coordinates = transform_wgs84_to_lv95(longitude, latitude, mode='approx')
    # Request elevation data
    # https://api3.geo.admin.ch/rest/services/height?easting=2600000&northing=1200000
    re = requests.get(
        swisstopo_elevation.format(
            easting=coordinates['easting'],
            northing=coordinates['northing']
        )
    )
    
    # Check if the request received some data
    if re.status_code == 200:
        return re.json()['height']


def add_elevation(gpx: gpxpy.gpx.GPX, mode='srtm'):
    """
    Add elevation data to gpx file
    """
    # Add elevation data
    if mode == 'srtm':
        elevation_data.add_elevations(gpx, smooth=True)
    elif mode == 'swisstopo':
        # Write elevation data into gpx object
        for point in gpx.walk(only_points=True):
            point.elevation = get_swisstopo_elevation(
                point.longitude,
                point.latitude
            )
    
    elif mode == 'polyline':
        re = requests.get(get_swisstopo_polyline_request(gpx))
        for idx, point in enumerate(gpx.walk(only_points=True)):
            point.elevation = re.json()[idx]['alts']['COMB']
            
    else:
        raise NotImplementedError('You are calling an option that is not implemented.')


if __name__ == '__main__':
    """
    Script to add elevation data to gpx files
    """
    import sys
    # from optparse import OptionParser
    # opt_parser = OptionParser()

    # Iterate over list of gpx files
    for arg in sys.argv[1:]:
        # Parse GPX file
        with open(arg, 'r') as file:
            gpx = gpxpy.parse(file)
    
        try:
            add_elevation(gpx, mode='swisstopo')
            print('Used swisstopo data.')
        except:
            add_elevation(gpx, mode='srtm')
            print('Used SRTM data.')

        # Overwrite input file
        with open(arg, 'w') as file:
            file.write(gpx.to_xml())
