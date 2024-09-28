import unittest
from gpx_elevation_adder.transformations import transform_wgs84_to_lv95


class TestTransformations(unittest.TestCase):

    def test_transform_wgs84_to_lv95_api(self):
        # Known coordinates for testing
        longitude = 8.5417  # Zurich longitude
        latitude = 47.3769  # Zurich latitude

        result = transform_wgs84_to_lv95(longitude, latitude, mode='api')
        self.assertIn('easting', result)
        self.assertIn('northing', result)
        self.assertIsInstance(result['easting'], float)
        self.assertIsInstance(result['northing'], float)

    def test_transform_wgs84_to_lv95_approx(self):
        longitude = 8.5417
        latitude = 47.3769

        result = transform_wgs84_to_lv95(longitude, latitude, mode='approx')
        self.assertIn('easting', result)
        self.assertIn('northing', result)
        self.assertIsInstance(result['easting'], float)
        self.assertIsInstance(result['northing'], float)

    def test_transform_wgs84_to_lv95_invalid_mode(self):
        longitude = 8.5417
        latitude = 47.3769

        with self.assertRaises(NotImplementedError):
            transform_wgs84_to_lv95(longitude, latitude, mode='invalid')


if __name__ == '__main__':
    unittest.main()
