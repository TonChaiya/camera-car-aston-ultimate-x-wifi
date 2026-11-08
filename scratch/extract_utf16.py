with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    f.seek(0x00293000)
    data = f.read(0x002A0000 - 0x00293000)

# Extract UTF-16LE strings of length >= 4
import re
# Look for 4 or more printable ASCII chars separated by null bytes
pattern = rb'(?:[\x20-\x7E]\x00){4,}'
matches = re.finditer(pattern, data)

print("UTF-16LE strings found:")
for m in matches:
    raw = m.group(0)
    text = raw.decode('utf-16le', errors='ignore')
    if any(k in text.lower() for k in ['cgi', 'camera', 'file', 'net', 'wifi', 'prop', 'action', 'set', 'get', 'dir', 'list', 'down', 'movie', 'photo', 'dcim', 'play', 'video']):
        print(f"  0x{0x00293000 + m.start():08X}: {text}")
