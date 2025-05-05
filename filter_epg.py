import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# Channels to filter
CHANNELS = [
    "ADA DERANA 24", "ART Television", "Buddhist TV", "Channel C", "Channel One", 
    "Citi Hitz", "Damsathara TV", "God TV/Swarga TV", "Haritha TV", "Hi TV", 
    "Hiru TV", "ITN", "Jaya TV", "Monara TV", "Nethra TV", "Pragna TV", 
    "Rangiri Sri Lanka", "Ridee TV", "Rupavahini", "Shakthi TV", "Shraddha TV", 
    "Sirasa TV", "Siyatha TV", "Supreme TV", "Swarnawahini Live", "Swarnawahini", 
    "TV Derana", "TV Didula", "TV1 Sri Lanka", "Vasantham TV"
]

# Input and output file paths
INPUT_FILE = "epg.xml.gz"
OUTPUT_FILE = "dialog.xml"

def validate_and_parse_xml(file):
    try:
        with gzip.open(file, 'rb') as f:
            tree = ET.parse(f)
        return tree
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return None

def filter_epg(input_file, output_file):
    # Validate and parse the XML
    tree = validate_and_parse_xml(input_file)
    if tree is None:
        print("Skipping processing due to XML errors.")
        return

    root = tree.getroot()

    # Get the current time and 24 hours later with timezone
    now = datetime.now(timezone.utc)
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
