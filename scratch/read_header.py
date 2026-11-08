import struct

with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    data = f.read(1024)

print("Offset 0x00 - 0x80:")
for i in range(0, 0x100, 16):
    hex_str = ' '.join(f'{b:02X}' for b in data[i:i+16])
    ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[i:i+16])
    print(f"{i:04X}: {hex_str}  {ascii_str}")
