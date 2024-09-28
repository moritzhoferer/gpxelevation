from typing import Dict
import requests

# Initialize a session for HTTP requests
session = requests.Session()

# API Endpoint
WGS84_TO_LV95 = 'http://geodesy.geo.admin.ch/reframe/wgs84tolv95?easting={lon:f}&northing={lat:f}&format=json'


def transform_wgs84_to_lv95(longitude: float, latitude: float, mode: str = 'api') -> Dict[str, float]:
    """Transform WGS84 coordinates to LV95.

    Args:
        longitude (float): Longitude in WGS84.
        latitude (float): Latitude in WGS84.
        mode (str, optional): Transformation mode ('api' or 'approx'). Defaults to 'api'.

    Returns:
        Dict[str, float]: A dictionary with 'easting' and 'northing' in LV95.

    Raises:
        NotImplementedError: If the mode is not implemented.
    """
    if mode == 'api':
        response = session.get(
            WGS84_TO_LV95.format(lon=longitude, lat=latitude)
        )
        response.raise_for_status()
        _dict = response.json()
        # Convert 'easting' and 'northing' to float
        _dict['easting'] = float(_dict['easting'])
        _dict['northing'] = float(_dict['northing'])
    elif mode == 'approx':
        # Approximate transformation
        # Source: Swiss Federal Office of Topography (swisstopo)
        # https://www.swisstopo.admin.ch/en/transformation-calculation-services
        _phi = (latitude * 3600.0 - 169028.66) / 10000.0
        _lambda = (longitude * 3600.0 - 26782.5) / 10000.0
        easting = (
            2600072.37
            + 211455.93 * _lambda
            - 10938.51 * _lambda * _phi
            - 0.36 * _lambda * _phi**2
            - 44.54 * _lambda**3
        )
        northing = (
            1200147.07
            + 308807.95 * _phi
            + 3745.25 * _lambda**2
            + 76.63 * _phi**2
            - 194.56 * _lambda**2 * _phi
            + 119.79 * _phi**3
        )
        _dict = {'easting': easting, 'northing': northing}
    else:
        raise NotImplementedError('Mode not implemented.')
    return _dict
