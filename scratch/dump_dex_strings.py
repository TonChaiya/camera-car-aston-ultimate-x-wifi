import zipfile, re

apk_path = r'c:\laragon\www\app-ios-astonCamera\tmcam-for-mstar-1-1-25082115.apk'

with zipfile.ZipFile(apk_path, 'r') as z:
    data = z.read('classes2.dex')

# Extract all ASCII/UTF-8 strings of length >= 3
strings = re.findall(rb'[\x20-\x7E]{3,}', data)
clean_strings = [s.decode('ascii', errors='ignore') for s in strings]

print(f"Total string tokens: {len(clean_strings)}")

keywords = [
    'Config.cgi', 'action=', 'property=', 'Camera.', 'getFileList', 'downloadFile',
    'DeviceApi', 'DeviceHttpEngine', 'DeviceRequest', 'FileListResponse', 'MediaFile',
    'CamIdResponse', 'Camid', 'Normal', 'Event', 'DCIM', 'MOVIE', 'PHOTO', 'http://',
    'thumb', 'playback', 'PLAYBACK', 'UIMode'
]

matching = {}
for kw in keywords:
    matching[kw] = [s for s in clean_strings if kw.lower() in s.lower()]
    print(f"\n--- Keyword: {kw} (Matches: {len(matching[kw])}) ---")
    for s in matching[kw][:15]:
        print(f"  {s}")
