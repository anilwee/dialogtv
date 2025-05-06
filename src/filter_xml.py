from lxml import etree
from datetime import datetime, timedelta

# Define the channels to keep
CHANNELS_TO_KEEP = {
    "ADA DERANA 24", "ART Television", "Buddhist TV", "Channel C", "Channel One",
    "Citi Hitz", "Damsathara TV", "God TV/Swarga TV", "Haritha TV", "Hi TV",
    "Hiru TV", "ITN", "Jaya TV", "Monara TV", "Nethra TV", "Pragna TV",
    "Rangiri Sri Lanka", "Ridee TV", "Rupavahini", "Shakthi TV", "Shraddha TV",
    "Sirasa TV", "Siyatha TV", "Supreme TV", "Swarnawahini Live", "Swarnawahini",
    "TV Derana", "TV Didula", "TV1 Sri Lanka", "Vasantham TV"
}

# Define the time threshold (48 hours from now)
time_threshold = datetime.utcnow() + timedelta(hours=48)

def filter_xml(input_file, output_file):
    # Parse the XML file with recovery
    try:
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(input_file, parser)
        root = tree.getroot()

        # Filter channels
        for channel in root.findall('.//channel'):
            channel_name = channel.find('name').text
            if channel_name not in CHANNELS_TO_KEEP:
                root.remove(channel)

        # Filter programs within the remaining channels
        for programme in root.findall('.//programme'):
            start_time = programme.get('start')
            start_datetime = datetime.strptime(start_time, "%Y%m%d%H%M%S %z").replace(tzinfo=None)

            if start_datetime > time_threshold:
                root.remove(programme)

        # Write the filtered XML to the output file
        tree.write(output_file, encoding='utf-8', pretty_print=True, xml_declaration=True)
        print(f"Filtered XML saved to {output_file}")

    except Exception as e:
        print(f"Error processing XML: {e}")

if __name__ == "__main__":
    input_file = "epg.xml"
    output_file = "public/dialog.xml"
    filter_xml(input_file, output_file)
