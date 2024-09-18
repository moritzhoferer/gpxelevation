#!/usr/bin/env python

import argparse
import logging
import os
import sys
import json
import requests
import gpxpy
import srtm as srtm_py
from urllib.parse import urlencode

# Initialize a session for HTTP requests
session = requests.Session()

# API Endpoints
WGS84_TO_LV95 = 'http://geodesy.geo.admin.ch/reframe/wgs84tolv95?easting={lon:f}&northing={lat:f}&format=json'
SWISSTOPO_ELEVATION = 'https://api3.geo.admin.ch/rest/services/height?easting={easting}&northing={northing}&sr=2056'

def transform_wgs84_to_lv95(longitude, latitude, mode='api') -> dict:
    """Transform WGS84 coordinates to LV95"""
    if mode == 'api':
        response = session.get(
            WGS84_TO_LV95.format(lon=longitude, lat=latitude)
        )
        response.raise_for_status()
        _dict = response.json()
    elif mode == 'approx':
        # Approximate transformation
        _phi = (float(latitude) * 3600. - 169028.66) / 1e4
        _lambda = (float(longitude) * 3600. - 26782.5) / 1e4
        easting = 2600072.37 + 211455.93 * _lambda - 10938.51 * _lambda * _phi \
            - 0.36 * _lambda * _phi**2 - 44.54 * _lambda**3
        northing = 1200147.07 + 308807.95 * _phi + 3745.25 * _lambda**2 + 76.63 * _phi**2 \
            - 194.56 * _lambda**2 * _phi + 119.79 * _phi**3
        _dict = {'easting': easting, 'northing': northing}
    else:
        raise NotImplementedError('Mode not implemented.')
    return _dict

def get_swisstopo_elevation(longitude, latitude) -> float:
    """Get elevation from Swisstopo API"""
    coordinates = transform_wgs84_to_lv95(longitude, latitude, mode='approx')
    response = session.get(
        SWISSTOPO_ELEVATION.format(
            easting=coordinates['easting'],
            northing=coordinates['northing']
        )
    )
    response.raise_for_status()
    return response.json()['height']

def add_elevation(gpx: gpxpy.gpx.GPX, mode='srtm'):
    """Add elevation data to GPX file"""
    # if mode == 'srtm':
    #     elevation_data = srtm.get_data()
    #     elevation_data.add_elevations(gpx, smooth=True)
    if mode == 'srtm':
        elevation_data = srtm_py.get_data()
        elevation_data.add_elevations(gpx, smooth=True)
    elif mode == 'swisstopo':
        for point in gpx.walk(only_points=True):
            point.elevation = get_swisstopo_elevation(
                point.longitude,
                point.latitude
            )
    elif mode == 'polyline':
        coordinates = []
        for point in gpx.walk(only_points=True):
            _coordinates = transform_wgs84_to_lv95(point.longitude, point.latitude)
            coordinates.append([_coordinates['easting'], _coordinates['northing']])
        geom = {
            "type": "LineString",
            "coordinates": coordinates
        }
        params = {
            'geom': json.dumps(geom),
            'sr': 2056,
            'nb_points': len(coordinates),
            'distinct_points': 'true'
        }
        response = session.get('https://api3.geo.admin.ch/rest/services/profile.json', params=params)
        response.raise_for_status()
        profile = response.json()
        for idx, point in enumerate(gpx.walk(only_points=True)):
            point.elevation = profile[idx]['alts']['COMB']
    else:
        raise NotImplementedError('Mode not implemented.')

def main():
    parser = argparse.ArgumentParser(
        description='Add elevation data to GPX files.'
    )
    parser.add_argument('input_files', nargs='+', help='GPX files to process')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('--mode', choices=['srtm', 'swisstopo', 'polyline'], default='swisstopo',
                        help='Method to use for adding elevation data')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite input files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    for input_file in args.input_files:
        logging.info(f'Processing file: {input_file}')
        with open(input_file, 'r') as file:
            gpx = gpxpy.parse(file)

        try:
            add_elevation(gpx, mode=args.mode)
            logging.info(f'Used {args.mode} data.')
        except Exception as e:
            logging.error(f'Failed to add elevation using {args.mode}: {e}')
            if args.mode != 'srtm':
                logging.info('Trying SRTM data as fallback.')
                try:
                    add_elevation(gpx, mode='srtm')
                    logging.info('Used SRTM data.')
                except Exception as e_srtm:
                    logging.error(f'Failed to add elevation using SRTM: {e_srtm}')
                    continue
            else:
                continue

        # Determine output file path
        if args.overwrite:
            output_file = input_file
        elif args.output:
            if len(args.input_files) > 1 and not os.path.isdir(args.output):
                logging.error('Output must be a directory when processing multiple files.')
                sys.exit(1)
            if os.path.isdir(args.output):
                output_file = os.path.join(args.output, os.path.basename(input_file))
            else:
                output_file = args.output
        else:
            output_file = input_file

        with open(output_file, 'w') as file:
            file.write(gpx.to_xml())
        logging.info(f'Written updated GPX to {output_file}')

if __name__ == '__main__':
    main()