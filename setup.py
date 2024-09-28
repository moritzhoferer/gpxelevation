from setuptools import setup, find_packages

setup(
    name='gpx-elevation-adder',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'gpxpy',
        'srtm.py',
    ],
    entry_points={
        'console_scripts': [
            'gpx-add-elevation=gpx_elevation_adder.main:run_main',
        ],
    },
    author='Moritz',
    author_email='moritzhoferer@gmail.com',
    description='A tool to add elevation data to GPX files',
    url='hhttps://moritzhoferer.github.io/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
