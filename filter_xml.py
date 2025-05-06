import xml.etree.ElementTree as ET

# Define the channels to keep
channels_to_keep = {
    "ADA DERANA 24", "ART Television", "Buddhist TV", "Channel C", "Channel One",
    "Citi Hitz", "Damsathara TV", "God TV/Swarga TV", "Haritha TV", "Hi TV",
    "Hiru TV", "ITN", "Jaya TV", "Monara TV", "Nethra TV", "Pragna TV",
    "Rangiri Sri Lanka", "Ridee TV", "Rupavahini", "Shakthi TV", "Shraddha TV",
    "Sirasa TV", "Siyatha TV", "Supreme TV", "Swarnawahini Live", "Swarnawahini",
    "TV Derana", "TV Didula", "TV1 Sri Lanka", "Vasantham TV"
}

# Parse the XML
tree = ET.parse('epg.xml')
root = tree.getroot()

# Filter the channels
for channel in root.findall('./channel'):
    name = channel.find('name').text
    if name not in channels_to_keep:
        root.remove(channel)

# Save the filtered XML
tree.write('dialog.xml')
