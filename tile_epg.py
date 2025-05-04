import xml.etree.ElementTree as ET
import sys

def tile_epg(input_file, output_file):
    # Parse the input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Create a new root for the tiled XML
    tiled_root = ET.Element('tv')

    # Group programs by time slots
    time_slots = {}
    for programme in root.findall('programme'):
        start_time = programme.attrib['start']
        channel = programme.attrib['channel']

        # Use start time as the key for grouping
        if start_time not in time_slots:
            time_slots[start_time] = []
        time_slots[start_time].append((channel, programme))

    # Create tiled structure
    for start_time, programs in sorted(time_slots.items()):
        timeslot = ET.SubElement(tiled_root, 'timeslot', {'start': start_time})
        for channel, programme in programs:
            channel_element = ET.SubElement(timeslot, 'channel', {'id': channel})
            channel_element.append(programme)

    # Write the tiled XML to the output file
    tiled_tree = ET.ElementTree(tiled_root)
    tiled_tree.write(output_file, encoding='utf-8', xml_declaration=True)

# Main script execution
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python tile_epg.py <input_epg.xml> <output_lktv.xml>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    tile_epg(input_file, output_file)
    print(f"Tiled EPG file created: {output_file}")
