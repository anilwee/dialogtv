import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Channels to filter
CHANNELS = [
    "Rupavahini", "ITN", "Sirasa TV", "Siyatha TV", "Swarnavahini", "Hiru TV",
    "TV Derana", "TNL", "Supreme TV", "Ridee TV", "Citi Hitz", "Channel Eye",
    "Nethra TV", "ART TV", "TV1", "Shakthi TV", "Vasantham TV", "Ada Derana 24",
    "Rangiri Sri Lanka", "The Buddhist TV", "Shraddha TV", "Hi TV"
]

# Input and output file paths
INPUT_FILE = "epg.xml.gz"
OUTPUT_FILE = "dialog.xml"

def filter_epg(input_file, output_file):
    # Decompress the gzipped input file
    with gzip.open(input_file, 'rb') as f:
        tree = ET.parse(f)
    root = tree.getroot()

    # Get the current time and 24 hours later
    now = datetime.now()
    end_time = now + timedelta(hours=24)

    # Filter the programs
    for channel in root.findall("./channel"):
        channel_name = channel.find("display-name").text
        if channel_name not in CHANNELS:
            root.remove(channel)

    for programme in root.findall("./programme"):
        start_time = datetime.strptime(programme.attrib["start"], "%Y%m%d%H%M%S %z")
        if programme.attrib["channel"] not in CHANNELS or start_time > end_time:
            root.remove(programme)

    # Write to output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    filter_epg(INPUT_FILE, OUTPUT_FILE)
