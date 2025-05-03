import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import os
import sys

# Channels to filter
CHANNELS = [
    "ADA DERANA 24", "ART Television", "Buddhist TV", "Channel C", "Channel One", 
    "Citi Hitz", "Damsathara TV", "God TV/Swarga TV", "Haritha TV", "Hi TV", 
    "Hiru TV", "ITN", "Jaya TV", "Monara TV", "Nethra TV", "Pragna TV", 
    "Rangiri Sri Lanka", "Ridee TV", "Rupavahini", "Shakthi TV", "Shraddha TV", 
    "Sirasa TV", "Siyatha TV", "Supreme TV", "Swarnawahini Live", "Swarnawahini", "TNL", 
    "TV Derana", "TV Didula", "TV1 Sri Lanka", "Vasantham TV"
]

# Input and output file paths
INPUT_FILE = "epg.xml.gz"
OUTPUT_FILE = "dialog.xml"

def filter_epg(input_file, output_file):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file '{input_file}' not found!")
        sys.exit(1)

    try:
        # Decompress the gzipped input file
        with gzip.open(input_file, 'rb') as f:
            tree = ET.parse(f)
        root = tree.getroot()

        # Get the current time and 24 hours later with timezone
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(hours=24)

        # Collect channels and programs to remove
        channels_to_remove = []
        programs_to_remove = []

        for channel in root.findall("./channel"):
            channel_name = channel.find("display-name").text
            if channel_name not in CHANNELS:
                channels_to_remove.append(channel)

        for programme in root.findall("./programme"):
            start_time = datetime.strptime(programme.attrib["start"], "%Y%m%d%H%M%S %z")
            if programme.attrib["channel"] not in CHANNELS or start_time > end_time:
                programs_to_remove.append(programme)

        # Remove filtered elements
        for channel in channels_to_remove:
            root.remove(channel)

        for programme in programs_to_remove:
            root.remove(programme)

        # Write to output file
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Filtered EPG saved to '{output_file}'.")

    except Exception as e:
        print(f"ERROR: Failed to process the EPG file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    filter_epg(INPUT_FILE, OUTPUT_FILE)
