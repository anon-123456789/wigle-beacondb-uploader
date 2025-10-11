#!/usr/bin/env python3
import argparse
import csv
import datetime

import requests
from tqdm import tqdm

geosubmit_url = "https://api.beacondb.net/v2/geosubmit"
geosubmit_user_agent = "wigle-beacondb-uploader/1.0 (https://github.com/anon-123456789/wigle-beacondb-uploader)"

file_length = 0
unique_locations = {}
number_bluetooth = 0
number_cellular = 0
number_wifi = 0

parser = argparse.ArgumentParser()
parser.add_argument("csv_file", help="CSV file obtained from the WiGLE app or API")
parser.add_argument("--submission-url", help="Use a specific URL to submit the data to, instead of the default one.")
parser.add_argument("--user-agent", help="Use a specific User-Agent string when submitting the data, instead of the default one.")
args = parser.parse_args()

if args.submission_url:
    geosubmit_url = args.submission_url
if args.user_agent:
    geosubmit_user_agent = args.user_agent

print(f"Submission URL set to \"{geosubmit_url}\"!")
print(f"User-Agent string set to \"{geosubmit_user_agent}\"!")

print(f"Calculating length of \"{args.csv_file}\"...")
with open(args.csv_file) as f:
    file_length = sum(1 for _ in f)

with open(args.csv_file, newline='') as file:
    reader = csv.reader(file)
    print(f"Processing \"{args.csv_file}\"...")
    for index, row in enumerate(tqdm(reader, total=file_length)):
        if index > 1:
            location_id = f"{row[3]}|{row[7]}|{row[8]}|{row[9]}|{row[10]}"
            if location_id not in unique_locations:
                unique_locations[location_id] = {"timestamp": int(datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp() * 1000), "position": {"latitude": float(row[7]), "longitude": float(row[8]), "accuracy": float(row[10]), "altitude": float(row[9])}, "bluetoothBeacons": [], "cellTowers": [], "wifiAccessPoints": []}
            match row[13]:
                case "BT":
                    try:
                        number_bluetooth += 1
                        unique_locations[location_id]["bluetoothBeacons"].append({"macAddress": row[0], "age": 0, "name": row[1], "signalStrength": int(row[6])})
                    except ValueError:
                        print(f"Failed to process the Bluetooth beacon with MAC {row[0]} on line {index}")
                case "BLE":
                    try:
                        number_bluetooth += 1
                        unique_locations[location_id]["bluetoothBeacons"].append({"macAddress": row[0], "age": 0, "name": row[1], "signalStrength": int(row[6])})
                    except ValueError:
                        print(f"Failed to process the Bluetooth beacon with MAC {row[0]} on line {index}")
                case "NR":
                    try:
                        unique_locations[location_id]["cellTowers"].append({"radioType": "nr", "mobileCountryCode": int(row[0].split("_")[0][:3]), "mobileNetworkCode": int(row[0].split("_")[0][-3:]), "locationAreaCode": int(row[0].split("_")[1]), "cellId": int(row[0].split("_")[2]), "age": 0, "signalStrength": int(row[6])})
                        number_cellular += 1
                    except ValueError:
                        print(f"Failed to process the NR network with identifier {row[0]} on line {index}")
                case "LTE":
                    try:
                        unique_locations[location_id]["cellTowers"].append({"radioType": "lte", "mobileCountryCode": int(row[0].split("_")[0][:3]), "mobileNetworkCode": int(row[0].split("_")[0][-3:]), "locationAreaCode": int(row[0].split("_")[1]), "cellId": int(row[0].split("_")[2]), "age": 0, "signalStrength": int(row[6])})
                        number_cellular += 1
                    except ValueError:
                        print(f"Failed to process the LTE network with identifier {row[0]} on line {index}")
                case "GSM":
                    try:
                        unique_locations[location_id]["cellTowers"].append({"radioType": "gsm", "mobileCountryCode": int(row[0].split("_")[0][:3]), "mobileNetworkCode": int(row[0].split("_")[0][-3:]), "locationAreaCode": int(row[0].split("_")[1]), "cellId": int(row[0].split("_")[2]), "age": 0, "signalStrength": int(row[6])})
                        number_cellular += 1
                    except ValueError:
                        print(f"Failed to process the GSM network with identifier {row[0]} on line {index}")
                case "WCDMA":
                    try:
                        unique_locations[location_id]["cellTowers"].append({"radioType": "wcdma", "mobileCountryCode": int(row[0].split("_")[0][:3]), "mobileNetworkCode": int(row[0].split("_")[0][-3:]), "locationAreaCode": int(row[0].split("_")[1]), "cellId": int(row[0].split("_")[2]), "age": 0, "signalStrength": int(row[6])})
                        number_cellular += 1
                    except ValueError:
                        print(f"Failed processing the WCDMA network with identifier {row[0]} on line {index}")
                case "WIFI":
                    try:
                        unique_locations[location_id]["wifiAccessPoints"].append({"macAddress": row[0], "age": 0, "channel": int(row[4]), "frequency": int(row[5]), "signalStrength": int(row[6]), "ssid": row[1]})
                        number_wifi += 1
                    except ValueError:
                        print(f"Failed processing the Wi-Fi network with MAC {row[0]} on line {index}")
                case _:
                    print(f"Unknown network type \"{row[13]}\" with identifier {row[0]} on line {index}")

print(f"Almost there! Processed {number_bluetooth} Bluetooth beacons, {number_cellular} cell towers, and {number_wifi} Wi-Fi networks, with {len(unique_locations)} unique locations.")

if number_bluetooth + number_cellular + number_wifi == 0:
    raise Exception("There doesn't seem to be any networks to submit. If you're sure that you're using a valid CSV file, please file an issue at https://github.com/anon-123456789/wigle-beacondb-uploader/issues")

print("Uploading the data (this may take a while)...")
request = requests.post(geosubmit_url, headers={"User-Agent": geosubmit_user_agent}, json={"items": list(unique_locations.values())})
request.raise_for_status()

print("Done! :)")