#!/usr/bin/env python

import argparse
import logging
import os
import sys
from typing import List, Optional

import gpxpy
import gpxpy.gpx

from gpx_elevation_adder.elevation import add_elevation
from gpx_elevation_adder.utils import setup_logging, log_exception


def process_file(input_file: str, output_file: Optional[str], mode: str, overwrite: bool) -> None:
    """Process a single GPX file.

    Args:
        input_file (str): Path to the input GPX file.
        output_file (Optional[str]): Path to the output GPX file.
        mode (str): Elevation data source mode.
        overwrite (bool): Whether to overwrite the input file.
    """
    logging.info(f'Processing file: {input_file}')
    try:
        with open(input_file, 'r') as file:
            gpx = gpxpy.parse(file)
    except Exception as e:
        log_exception(e, f'Failed to read GPX file {input_file}')
        return

    try:
        add_elevation(gpx, mode=mode)
        logging.info(f'Used {mode} data.')
    except Exception as e:
        log_exception(e, f'Failed to add elevation using {mode}')
        if mode != 'srtm':
            logging.info('Trying SRTM data as fallback.')
            try:
                add_elevation(gpx, mode='srtm')
                logging.info('Used SRTM data.')
            except Exception as e_srtm:
                log_exception(e_srtm, 'Failed to add elevation using SRTM')
                return
        else:
            return

    if overwrite and output_file is None:
        output_file = input_file
    elif output_file is None:
        output_file = input_file

    try:
        with open(output_file, 'w') as file:
            file.write(gpx.to_xml())
        logging.info(f'Written updated GPX to {output_file}')
    except Exception as e:
        log_exception(e, f'Failed to write GPX file {output_file}')


def run_main() -> None:
    """Main function to parse arguments and process GPX files."""
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

    setup_logging(args.verbose)

    if args.output and len(args.input_files) > 1 and not os.path.isdir(args.output):
        logging.error('Output must be a directory when processing multiple files.')
        sys.exit(1)

    for input_file in args.input_files:
        if not os.path.isfile(input_file):
            logging.error(f'Input file does not exist: {input_file}')
            continue

        if args.overwrite:
            output_file = input_file
        elif args.output:
            if os.path.isdir(args.output):
                output_file = os.path.join(args.output, os.path.basename(input_file))
            else:
                output_file = args.output
        else:
            output_file = None

        process_file(input_file, output_file, args.mode, args.overwrite)


if __name__ == '__main__':
    run_main()
