# wigle-beacondb-uploader
This is a Python script that automatically converts [WiGLE CSV files](https://api.wigle.net/csvFormat.html) to the [Ichnaea/MLS geosubmit](https://ichnaea.readthedocs.io/en/latest/api/geosubmit2.html) format, then submits that data to [BeaconDB](https://beacondb.net).

> [!IMPORTANT]
> This script does not attempt to validate input files, for the most part. **Unexpected things may happen if you give it malformed input files.**

## Usage
You can get the CSV file from the WiGLE Android App to use your local database, or you could use [this tool (untested)](https://github.com/joelkoen/wigledl) to use the data that you've uploaded previously. **Only one file is accepted for each run.**
```bash
# Clone the repo
git clone https://github.com/anon-123456789/wigle-beacondb-uploader.git
cd wigle-beacondb-uploader

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Actually run it
python3 uploader.py /path/to/your/file.csv
```

## Options
```
usage: uploader.py [-h] [--submission-url SUBMISSION_URL] [--user-agent USER_AGENT] csv_file

positional arguments:
  csv_file              CSV file obtained from the WiGLE app or API

options:
  -h, --help            show this help message and exit
  --submission-url SUBMISSION_URL
        Use a specific URL to submit the data to, instead of the default one.
  --user-agent USER_AGENT
        Use a specific User-Agent string when submitting the data, instead of the default one.
```

## Example Output
```
$ python3 uploader.py /path/to/your/file.csv
Submission URL set to "https://api.beacondb.net/v2/geosubmit"!
User-Agent string set to "wigle-beacondb-uploader/1.0 (https://github.com/anon-123456789/wigle-beacondb-uploader)"!
Calculating length of "/path/to/your/file.csv"...
Processing "/path/to/your/file.csv"...
<progress bar would be displayed here>
Almost there! Processed 9999 Bluetooth beacons, 9999 cell towers, and 9999 Wi-Fi networks, with 9999 unique locations.
Uploading the data (this may take a while)...
Done! :)
```

## Disclaimer
> [!IMPORTANT]
> This project is not affiliated in any way with WiGLE or BeaconDB.

## License
wigle-beacondb-uploader
<br>
Copyright &copy; 2025 anon-123456789

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.