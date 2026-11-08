import os, re

with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    data = f.read()

targets = [
    'Camera', 'Camera.File', 'DBFile', 'NormalDB', 'Config.cgi', 'action',
    'property', 'UIMode', 'FWversion', 'SD_CarDV', 'Redsonic', 'redsonic',
    'playback', 'PLAYBACK', 'DCIM', 'MOVIE', 'PHOTO', 'AIT', 'dir', 'file'
]

print(f"Total file size: {len(data)} bytes")
for t in targets:
    pos_asc = data.find(t.encode('ascii'))
    pos_utf = data.find(t.encode('utf-16le'))
    m = re.search(re.escape(t.encode('ascii')), data, re.IGNORECASE)
    pos_ci = m.start() if m else -1
    print(f"{t:15}: ASCII={pos_asc:08X} UTF16={pos_utf:08X} CI={pos_ci:08X}")
