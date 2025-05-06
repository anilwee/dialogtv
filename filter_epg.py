import os
import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Channels to filter
CHANNELS = [
    "ADA DERANA 24", "ART Television", "Buddhist TV", "Channel C", "Channel One",
    "Citi Hitz", "Damsathara TV", "God TV/Swarga TV", "Haritha TV", "Hi TV", 
    "Hiru TV", "ITN", "Jaya TV", "Monara TV", "Nethra TV", "Pragna TV",
    "Rangiri Sri Lanka", "Ridee TV", "Rupavahini", "Shakthi TV", "Shraddha TV",
    "Sirasa TV", "Siyatha TV", "Supreme TV", "Swarnawahini Live", "Swarnawahini", 
    "TV Derana", "TV Didula", "TV1 Sri Lanka", "Vasantham TV"
]

def filter_epg(input_file, output_file):
    # Parse the input XML
    with gzip.open(input_file, 'rb') as f:
        tree = ET.parse(f)
    root = tree.getroot()

    # Current time and 48-hour threshold
    now = datetime.utcnow()
    cutoff = now + timedelta(hours=48)

    # Filter channels and programmes
    filtered_tv = ET.Element("tv")
    for channel in root.findall("channel"):
        if channel.find("display-name").text in CHANNELS:
            filtered_tv.append(channel)

    for programme in root.findall("programme"):
        start_time = datetime.strptime(programme.get("start")[:14], "%Y%m%d%H%M%S")
        channel = programme.get("channel")
        if start_time <= cutoff and any(ch.find("display-name").text == channel for ch in filtered_tv.findall("channel")):
            filtered_tv.append(programme)

    # Write the filtered XML to the output file
    tree = ET.ElementTree(filtered_tv)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    # Input and output paths
    input_path = os.environ.get("CRITICAL_LINK")
    output_path = "dialog.xml"

    # Download and process the file
    filter_epg(input_path, output_path)
    print(f"Filtered EPG saved to {output_path}")
