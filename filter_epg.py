import gzip
import os
import xml.etree.ElementTree as ET

# Channels to filter
CHANNELS = [
    "ADA DERANA 24", "ART Television", "Buddhist TV", "Channel C", "Channel One",
    "Citi Hitz", "Damsathara TV", "God TV/Swarga TV", "Haritha TV", "Hi TV",
    "Hiru TV", "ITN", "Jaya TV", "Monara TV", "Nethra TV", "Pragna TV",
    "Rangiri Sri Lanka", "Ridee TV", "Rupavahini", "Shakthi TV", "Shraddha TV",
    "Sirasa TV", "Siyatha TV", "Supreme TV", "Swarnawahini Live", "Swarnawahini",
    "TV Derana", "TV Didula", "TV1 Sri Lanka", "Vasantham TV"
]

INPUT_FILE = "epg.xml.gz"
OUTPUT_FILE = "dialog.xml"

def is_gzip_file(filepath):
    with open(filepath, 'rb') as f:
        magic = f.read(2)
        return magic == b'\x1f\x8b'  # Gzip magic number

def filter_epg(input_file, output_file):
    if is_gzip_file(input_file):
        # Decompress the gzipped input file
        with gzip.open(input_file, 'rb') as f:
            tree = ET.parse(f)
    else:
        # Handle plain XML file
        with open(input_file, 'rb') as f:
            tree = ET.parse(f)
    
    root = tree.getroot()

    # Filter the XML tree
    for channel in root.findall("./channel"):
        channel_name = channel.find("display-name").text
        if channel_name not in CHANNELS:
            root.remove(channel)

    for programme in root.findall("./programme"):
        if programme.attrib["channel"] not in CHANNELS:
            root.remove(programme)

    # Write the filtered XML to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    filter_epg(INPUT_FILE, OUTPUT_FILE)
