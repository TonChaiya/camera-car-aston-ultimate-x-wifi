import zipfile, re, json

apk_path = r'c:\laragon\www\app-ios-astonCamera\tmcam-for-mstar-1-1-25082115.apk'

with zipfile.ZipFile(apk_path, 'r') as z:
    dex = z.read('classes2.dex')

# Target keywords
keywords = [
    'Config.cgi', 'action=', 'property=', 'Camera.Preview.Source.1.Camid',
    'CamIdResponse', 'FileListResponse', 'getFileList', 'downloadFile',
    'MediaFile', 'MediaDataAccess', 'DeviceApi', 'DeviceHttpEngine', 'DeviceRequest',
    'Normal', 'Event', 'DCIM', 'MOVIE', 'PHOTO', 'UIMode', 'PLAYBACK', 'thumb'
]

# Extract strings from DEX format properly
# In DEX, string_ids are at offset header+56 (string_ids_size, string_ids_off)
import struct
magic = dex[:8]
string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)

print(f"DEX string_ids_size: {string_ids_size}, off: {string_ids_off}")

extracted = set()
for i in range(string_ids_size):
    str_data_off = struct.unpack_from('<I', dex, string_ids_off + i * 4)[0]
    # read MUTF-8 length (uleb128)
    pos = str_data_off
    # skip uleb128
    while dex[pos] & 0x80:
        pos += 1
    pos += 1
    # null terminated string
    end = dex.find(b'\x00', pos)
    if end != -1 and end - pos < 500:
        try:
            s = dex[pos:end].decode('utf-8')
            extracted.add(s)
        except Exception:
            pass

print(f"Extracted unique DEX strings: {len(extracted)}")

summary = {}
for kw in keywords:
    matches = [s for s in extracted if kw.lower() in s.lower()]
    summary[kw] = matches

with open(r'c:\laragon\www\app-ios-astonCamera\scratch\dex_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("Saved to dex_summary.json")
