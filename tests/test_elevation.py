import unittest
from unittest.mock import patch
import gpxpy
from gpx_elevation_adder.elevation import (
    get_swisstopo_elevation,
    add_elevation_srtm,
    add_elevation_swisstopo,
    add_elevation_polyline,
)


class TestElevation(unittest.TestCase):

    def setUp(self):
        # Create a simple GPX object for testing
        self.gpx = gpxpy.gpx.GPX()
        track = gpxpy.gpx.GPXTrack()
        self.gpx.tracks.append(track)
        segment = gpxpy.gpx.GPXTrackSegment()
        track.segments.append(segment)
        segment.points.append(gpxpy.gpx.GPXTrackPoint(47.3769, 8.5417))  # Zurich

    @patch('gpx_elevation_adder.elevation.transform_wgs84_to_lv95')
    @patch('gpx_elevation_adder.elevation.session.get')
    def test_get_swisstopo_elevation(self, mock_get, mock_transform):
        mock_transform.return_value = {'easting': 2683200.0, 'northing': 1243300.0}
        mock_get.return_value.json.return_value = {'height': 408.0}
        mock_get.return_value.raise_for_status = lambda: None

        elevation = get_swisstopo_elevation(8.5417, 47.3769)
        self.assertEqual(elevation, 408.0)

    def test_add_elevation_srtm(self):
        # This test requires SRTM data, which may not be available offline.
        try:
            add_elevation_srtm(self.gpx)
            point = next(self.gpx.walk(only_points=True))
            self.assertIsNotNone(point.elevation)
        except Exception as e:
            self.fail(f'add_elevation_srtm failed with exception: {e}')

    @patch('gpx_elevation_adder.elevation.get_swisstopo_elevation')
    def test_add_elevation_swisstopo(self, mock_get_elevation):
        mock_get_elevation.return_value = 408.0
        add_elevation_swisstopo(self.gpx)
        point = next(self.gpx.walk(only_points=True))
        self.assertEqual(point.elevation, 408.0)

    @patch('gpx_elevation_adder.elevation.transform_wgs84_to_lv95')
    @patch('gpx_elevation_adder.elevation.session.get')
    def test_add_elevation_polyline(self, mock_get, mock_transform):
        mock_transform.return_value = {'easting': 2683200.0, 'northing': 1243300.0}
        mock_get.return_value.json.return_value = [
            {'alts': {'COMB': 408.0}}
        ]
        mock_get.return_value.raise_for_status = lambda: None

        add_elevation_polyline(self.gpx)
        point = next(self.gpx.walk(only_points=True))
        self.assertEqual(point.elevation, 408.0)


if __name__ == '__main__':
    unittest.main()
