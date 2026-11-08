import os, gzip, lzma, zlib

with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    data = f.read()

# Let's search for gzip streams
print("Searching for gzip streams...")
import re
for m in re.finditer(rb'\x1f\x8b\x08', data):
    pos = m.start()
    try:
        decomp = gzip.decompress(data[pos:])
        print(f"GZIP found at 0x{pos:08X}, decompressed size: {len(decomp)}")
        if b'UIMode' in decomp:
            print("  FOUND UIMode in GZIP!")
        if b'PLAYBACK' in decomp:
            print("  FOUND PLAYBACK in GZIP!")
        if b'Camera.File' in decomp:
            print("  FOUND Camera.File in GZIP!")
    except Exception:
        pass

# Search for zlib streams
print("Searching for zlib streams...")
for m in re.finditer(rb'\x78[\x01\x5e\x9c\xda]', data[:500000]):
    pos = m.start()
    try:
        decomp = zlib.decompress(data[pos:])
        if len(decomp) > 1000:
            print(f"ZLIB found at 0x{pos:08X}, decompressed size: {len(decomp)}")
            if b'UIMode' in decomp or b'PLAYBACK' in decomp or b'Camera' in decomp:
                print(f"  Keywords in ZLIB at 0x{pos:08X}")
    except Exception:
        pass
