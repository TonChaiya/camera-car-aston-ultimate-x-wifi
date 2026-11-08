import zipfile, struct, json

with open(r'c:\laragon\www\app-ios-astonCamera\tmcam-for-mstar-1-1-25082115.apk', 'rb') as f:
    z = zipfile.ZipFile(f)
    dex = z.read('classes2.dex')

# Parse DEX class definitions
# class_defs_size @ offset 96, class_defs_off @ offset 100
class_defs_size, class_defs_off = struct.unpack_from('<II', dex, 96)
string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)
type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)

def get_string(idx):
    str_data_off = struct.unpack_from('<I', dex, string_ids_off + idx * 4)[0]
    pos = str_data_off
    while dex[pos] & 0x80:
        pos += 1
    pos += 1
    end = dex.find(b'\x00', pos)
    return dex[pos:end].decode('utf-8', errors='replace')

def get_type(idx):
    descriptor_idx = struct.unpack_from('<I', dex, type_ids_off + idx * 4)[0]
    return get_string(descriptor_idx)

print(f"Total classes in classes2.dex: {class_defs_size}")

mstar_classes = []
for i in range(class_defs_size):
    class_idx, access_flags, superclass_idx, interfaces_off, source_file_idx, annotations_off, class_data_off, static_values_off = struct.unpack_from('<IIIIIIII', dex, class_defs_off + i * 32)
    cname = get_type(class_idx)
    if 'com/tima/app' in cname or 'mstar' in cname:
        mstar_classes.append((cname, class_data_off))

print(f"Found {len(mstar_classes)} matching classes in com/tima/app")
for cname, off in mstar_classes:
    print(" ", cname)
