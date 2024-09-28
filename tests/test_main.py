import unittest
from unittest.mock import patch, mock_open
import gpx_elevation_adder.main as main_module


class TestMain(unittest.TestCase):

    @patch('gpx_elevation_adder.main.add_elevation')
    @patch('builtins.open', new_callable=mock_open, read_data='<gpx></gpx>')
    def test_process_file(self, mock_file, mock_add_elevation):
        input_file = 'test_input.gpx'
        output_file = 'test_output.gpx'
        mode = 'srtm'
        overwrite = False

        main_module.process_file(input_file, output_file, mode, overwrite)

        mock_file.assert_any_call(input_file, 'r')
        mock_file.assert_any_call(output_file, 'w')
        self.assertTrue(mock_add_elevation.called)

    @patch('gpx_elevation_adder.utils.logging')  # Patch logging in utils.py
    @patch('gpx_elevation_adder.main.add_elevation', side_effect=Exception('Test exception'))
    @patch('builtins.open', new_callable=mock_open, read_data='<gpx></gpx>')
    def test_process_file_add_elevation_exception(self, mock_file, mock_add_elevation, mock_logging):
        input_file = 'test_input.gpx'
        output_file = 'test_output.gpx'
        mode = 'srtm'
        overwrite = False

        main_module.process_file(input_file, output_file, mode, overwrite)

        self.assertTrue(mock_logging.error.called)
        self.assertTrue(mock_add_elevation.called)

if __name__ == '__main__':
    unittest.main()
