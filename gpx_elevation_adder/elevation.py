from typing import Optional, List, Dict
import json
import requests
import gpxpy.gpx
import srtm
from gpx_elevation_adder.transformations import transform_wgs84_to_lv95

# Initialize a session for HTTP requests
session = requests.Session()

# API Endpoint
SWISSTOPO_ELEVATION = "https://api3.geo.admin.ch/rest/services/height?easting={easting}&northing={northing}&sr=2056"


def get_swisstopo_elevation(longitude: float, latitude: float) -> Optional[float]:
    """Get elevation from Swisstopo API.

    Args:
        longitude (float): Longitude in WGS84.
        latitude (float): Latitude in WGS84.

    Returns:
        Optional[float]: Elevation in meters or None if failed.
    """
    coordinates = transform_wgs84_to_lv95(longitude, latitude, mode="approx")
    response = session.get(
        SWISSTOPO_ELEVATION.format(
            easting=coordinates["easting"], northing=coordinates["northing"]
        )
    )
    response.raise_for_status()
    data = response.json()
    return data.get("height")


def add_elevation_srtm(gpx: gpxpy.gpx.GPX) -> None:
    """Add elevation data to GPX using SRTM data.

    Args:
        gpx (gpxpy.gpx.GPX): The GPX object to modify.
    """
    elevation_data = srtm.get_data()
    elevation_data.add_elevations(gpx, smooth=True)


def add_elevation_swisstopo(gpx: gpxpy.gpx.GPX) -> None:
    """Add elevation data to GPX using Swisstopo data.

    Args:
        gpx (gpxpy.gpx.GPX): The GPX object to modify.
    """
    for point in gpx.walk(only_points=True):
        elevation = get_swisstopo_elevation(point.longitude, point.latitude)
        point.elevation = elevation


def add_elevation_polyline(gpx: gpxpy.gpx.GPX) -> None:
    """Add elevation data to GPX using Swisstopo polyline API.

    Args:
        gpx (gpxpy.gpx.GPX): The GPX object to modify.
    """
    coordinates = []
    for point in gpx.walk(only_points=True):
        coord = transform_wgs84_to_lv95(point.longitude, point.latitude)
        coordinates.append([coord["easting"], coord["northing"]])
    geom = {"type": "LineString", "coordinates": coordinates}
    params = {
        "geom": json.dumps(geom),
        "sr": 2056,
        "nb_points": len(coordinates),
        "distinct_points": "true",
    }
    response = session.get(
        "https://api3.geo.admin.ch/rest/services/profile.json", params=params
    )
    response.raise_for_status()
    profile = response.json()
    for idx, point in enumerate(gpx.walk(only_points=True)):
        point.elevation = profile[idx]["alts"]["COMB"]


def add_elevation(gpx: gpxpy.gpx.GPX, mode: str = "srtm") -> None:
    """Add elevation data to GPX file.

    Args:
        gpx (gpxpy.gpx.GPX): The GPX object to modify.
        mode (str, optional): Method to use ('srtm', 'swisstopo', 'polyline'). Defaults to 'srtm'.

    Raises:
        NotImplementedError: If the mode is not implemented.
    """
    if mode == "srtm":
        add_elevation_srtm(gpx)
    elif mode == "swisstopo":
        add_elevation_swisstopo(gpx)
    elif mode == "polyline":
        add_elevation_polyline(gpx)
    else:
        raise NotImplementedError(f"Mode {mode} not implemented.")
