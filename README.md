# GPX Elevation Adder

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  <!-- - [Install via pip](#install-via-pip) -->
  - [Install from Source](#install-from-source)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
  - [Examples](#examples)
- [Development](#development)
  - [Setting Up the Development Environment](#setting-up-the-development-environment)
  - [Running Tests](#running-tests)
  - [Code Style and Linting](#code-style-and-linting)
- [Dependencies](#dependencies)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Introduction

**GPX Elevation Adder** is a Python tool that adds elevation data to GPX files. It supports multiple elevation data sources, including SRTM and Swisstopo APIs, providing accurate elevation profiles for your GPS tracks.

## Features

- **Multiple Elevation Sources**:
  - **SRTM Data**: Global elevation data.
  - **Swisstopo Elevation API**: High-resolution elevation data for Switzerland.
  - **Swisstopo Polyline API**: Efficient elevation data retrieval for polylines.
- **Flexible Output Options**:
  - Overwrite existing GPX files.
  - Save to new files or directories.
- **Batch Processing**:
  - Process multiple GPX files at once.
- **Verbose Logging**:
  - Optional detailed logging for troubleshooting.

## Installation

### Prerequisites

- Python 3.6 or higher.
- `pip` package manager.

<!-- ### Install via pip

*(Note: The package needs to be published to PyPI for this method to work. If not yet published, use [Install from Source](#install-from-source).)*

```bash
pip install gpx-elevation-adder
``` -->

### Install from Source

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/moritzhoferer/gpx-elevation-adder.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd gpx-elevation-adder
   ```

3. **Install the Package**:

   ```bash
   pip install .
   ```

   For development mode (editable install):

   ```bash
   pip install -e .
   ```

## Usage

### Command-Line Interface

After installation, the `gpx-add-elevation` command-line tool is available.

```bash
gpx-add-elevation [-h] [-o OUTPUT] [--mode {srtm,swisstopo,polyline}] [--overwrite] [-v] input_files [input_files ...]
```

#### Arguments

- `input_files`: One or more GPX files to process.
- `-o`, `--output`: Output file or directory.
- `--mode`: Method to use for adding elevation data (`srtm`, `swisstopo`, or `polyline`). Defaults to `swisstopo`.
- `--overwrite`: Overwrite input files.
- `-v`, `--verbose`: Increase output verbosity.

#### Help

To display the help message:

```bash
gpx-add-elevation --help
```

### Examples

**Add elevation data using SRTM:**

```bash
gpx-add-elevation path/to/track.gpx --mode srtm -v
```

**Add elevation data using Swisstopo API and save to a new file:**

```bash
gpx-add-elevation path/to/track.gpx -o path/to/output.gpx --mode swisstopo
```

**Process multiple files and save to an output directory:**

```bash
gpx-add-elevation path/to/track1.gpx path/to/track2.gpx -o path/to/output_directory/
```

**Overwrite the original GPX files with new elevation data:**

```bash
gpx-add-elevation path/to/*.gpx --overwrite
```

## Development

### Setting Up the Development Environment

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/moritzhoferer/gpx-elevation-adder.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd gpx-elevation-adder
   ```

3. **Create and Activate a Virtual Environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows use venv\Scripts\activate
   ```

4. **Install the Package in Editable Mode with Development Dependencies**:

   ```bash
   pip install -e .
   pip install -r dev-requirements.txt
   ```

### Running Tests

We use `pytest` for testing. Tests are located in the `tests/` directory.

```bash
pytest tests/
```

### Code Style and Linting

We recommend using `flake8` and `black` for code style checks and formatting.

**Install Code Style Tools**:

```bash
pip install flake8 black
```

**Run Flake8**:

```bash
flake8 gpx_elevation_adder/ tests/
```

**Run Black**:

```bash
black gpx_elevation_adder/ tests/
```

## Dependencies

- [requests](https://pypi.org/project/requests/)
- [gpxpy](https://pypi.org/project/gpxpy/)
- [srtm.py](https://pypi.org/project/srtm.py/)
- [pytest](https://pypi.org/project/pytest/) (for development/testing)
- [flake8](https://pypi.org/project/flake8/) and [black](https://pypi.org/project/black/) (for code style/linting)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **SRTM Data**: Shuttle Radar Topography Mission data used for global elevation data.
- **Swisstopo**: Federal Office of Topography in Switzerland, providing high-resolution elevation data.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/moritzhoferer/gpx-elevation-adder) or contact me at [moritzhoferer@gmail.com](mailto:moritzhoferer@gmail.com).

## Additional Notes

- **API Usage**: When using the Swisstopo APIs, ensure you comply with their [terms of service](https://www.swisstopo.admin.ch/en/terms-of-use-free-geodata-and-geoservices).
- **Error Handling**: The tool attempts to use the specified elevation data source and falls back to SRTM data if it fails.
- **Logging**: Use the `--verbose` flag to enable detailed logging for troubleshooting.

---

<!-- ## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

--- -->

## Version History

- **v0.1.0**: Initial release with basic functionality.

---

## Frequently Asked Questions (FAQ)

### **Q**: What is GPX?

**A**: GPX (GPS Exchange Format) is an XML schema designed as a common GPS data format for software applications.

### **Q**: Why is elevation data missing from my GPX files?

**A**: Some devices or applications may not record elevation data, or you may have GPS tracks without elevation information. This tool helps add accurate elevation data based on geographic coordinates.

P.S.: I like choose skitours and downloading route file from [skitourenguru](https://www.skitourenguru.ch/). Their files come without elevation data. This was the reason to start this project.

### **Q**: Can I use this tool for locations outside Switzerland?

**A**: Yes. When using the `srtm` mode, the tool uses global SRTM data. However, the `swisstopo` and `polyline` modes provide high-resolution data only for Switzerland.

---

## Disclaimer

This tool is provided "as is" without warranty of any kind. It's a exercise for me and I used much support by [ChatGPT](https://chatgpt.com/) modells 4o and o1-preview. The author is not responsible for any damages or data loss that may occur as a result of using this tool.

---
