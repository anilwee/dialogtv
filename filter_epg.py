import re
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

INPUT_FILE = "epg.xml"
OUTPUT_FILE = "dialog.xml"

def clean_invalid_chars(xml_content):
    """
    Remove invalid XML characters from the content.
    """
    # Define a regex pattern for valid XML characters
    valid_xml_pattern = re.compile(
        r'[^\x09\x0A\x0D\x20-\xD7FF\xE000-\xFFFD\x10000-\x10FFFF]'
    )
    return valid_xml_pattern.sub('', xml_content)

def filter_epg(input_file, output_file):
    # Read and clean the XML content
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        cleaned_content = clean_invalid_chars(raw_content)

    # Parse the cleaned XML content
    root = ET.fromstring(cleaned_content)

    # Filter channels
    for channel in root.findall("./channel"):
        channel_name = channel.find("display-name").text
        if channel_name not in CHANNELS:
            root.remove(channel)

    # Filter programmes
    for programme in root.findall("./programme"):
        if programme.attrib["channel"] not in CHANNELS:
            root.remove(programme)

    # Write the filtered XML to the output file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    filter_epg(INPUT_FILE, OUTPUT_FILE)
