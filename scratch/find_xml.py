with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    data = f.read()

import re
matches = re.finditer(rb'[a-zA-Z0-9_\-\.\/]+\.xml', data, re.IGNORECASE)
seen = set()
for m in matches:
    path = m.group(0).decode('ascii', 'ignore')
    if path not in seen:
        seen.add(path)
        print(f'0x{m.start():08X}: {path}')
