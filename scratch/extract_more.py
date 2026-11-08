with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    f.seek(0x00297800)
    data = f.read(0x002B0000 - 0x00297800)

import re
# Check for any printable ASCII or UTF-16 strings
for m in re.finditer(rb'[\x20-\x7E]{5,}', data):
    s = m.group(0).decode('ascii', errors='ignore')
    if any(k in s.lower() for k in ['cgi', 'camera', 'file', 'http', 'dcim', 'video', 'movie', 'photo', 'play', 'down', 'dir', 'list', 'db', 'sd']):
        print(f"ASCII  0x{0x00297800 + m.start():08X}: {s[:100]}")

for m in re.finditer(rb'(?:[\x20-\x7E]\x00){5,}', data):
    s = m.group(0).decode('utf-16le', errors='ignore')
    if any(k in s.lower() for k in ['cgi', 'camera', 'file', 'http', 'dcim', 'video', 'movie', 'photo', 'play', 'down', 'dir', 'list', 'db', 'sd']):
        print(f"UTF16  0x{0x00297800 + m.start():08X}: {s[:100]}")
