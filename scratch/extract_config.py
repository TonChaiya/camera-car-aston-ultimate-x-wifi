with open(r'c:\laragon\www\app-ios-astonCamera\SD_CarDV.bin', 'rb') as f:
    f.seek(0x003A6A00)
    data = f.read(0x003AA000 - 0x003A6A00)

clean = ""
for b in data:
    if 32 <= b <= 126 or b in (10, 13, 9):
        clean += chr(b)
    else:
        clean += "\n"

lines = [line.strip() for line in clean.splitlines() if len(line.strip()) > 3]
print(f"Total config lines: {len(lines)}")
for line in lines[:80]:
    print(" ", line)
