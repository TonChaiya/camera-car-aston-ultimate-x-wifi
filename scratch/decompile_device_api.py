import zipfile, struct, json

with open(r'c:\laragon\www\app-ios-astonCamera\tmcam-for-mstar-1-1-25082115.apk', 'rb') as f:
    z = zipfile.ZipFile(f)
    dex = z.read('classes2.dex')

string_ids_size, string_ids_off = struct.unpack_from('<II', dex, 56)
type_ids_size, type_ids_off = struct.unpack_from('<II', dex, 64)
proto_ids_size, proto_ids_off = struct.unpack_from('<II', dex, 72)
field_ids_size, field_ids_off = struct.unpack_from('<II', dex, 80)
method_ids_size, method_ids_off = struct.unpack_from('<II', dex, 88)
class_defs_size, class_defs_off = struct.unpack_from('<II', dex, 96)

def get_string(idx):
    if idx >= string_ids_size:
        return f"<invalid_str_{idx}>"
    str_data_off = struct.unpack_from('<I', dex, string_ids_off + idx * 4)[0]
    pos = str_data_off
    while dex[pos] & 0x80:
        pos += 1
    pos += 1
    end = dex.find(b'\x00', pos)
    return dex[pos:end].decode('utf-8', errors='replace')

def get_type(idx):
    if idx >= type_ids_size:
        return f"<invalid_type_{idx}>"
    descriptor_idx = struct.unpack_from('<I', dex, type_ids_off + idx * 4)[0]
    return get_string(descriptor_idx)

def get_method(idx):
    if idx >= method_ids_size:
        return "<invalid_class>", f"<invalid_method_{idx}>"
    class_idx, proto_idx, name_idx = struct.unpack_from('<HHI', dex, method_ids_off + idx * 8)
    return get_type(class_idx), get_string(name_idx)

def get_field(idx):
    if idx >= field_ids_size:
        return "<invalid_class>", f"<invalid_field_{idx}>", "<invalid_type>"
    class_idx, type_idx, name_idx = struct.unpack_from('<HHI', dex, field_ids_off + idx * 8)
    return get_type(class_idx), get_string(name_idx), get_type(type_idx)

def read_uleb128(data, pos):
    result = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        result |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return result, pos

target_names = [
    'DeviceApi', 'DeviceHttpEngine', 'DeviceRequest', 'FileListResponse',
    'MediaFile', 'MediaDataAccess', 'CamIdResponse'
]

results = {}

for i in range(class_defs_size):
    class_idx, access_flags, superclass_idx, interfaces_off, source_file_idx, annotations_off, class_data_off, static_values_off = struct.unpack_from('<IIIIIIII', dex, class_defs_off + i * 32)
    cname = get_type(class_idx)
    matched = any(t in cname for t in target_names)
    if not matched:
        continue
    
    class_info = {"name": cname, "methods": [], "fields": []}
    
    if class_data_off != 0:
        pos = class_data_off
        static_fields_size, pos = read_uleb128(dex, pos)
        instance_fields_size, pos = read_uleb128(dex, pos)
        direct_methods_size, pos = read_uleb128(dex, pos)
        virtual_methods_size, pos = read_uleb128(dex, pos)
        
        # static fields
        field_idx = 0
        for _ in range(static_fields_size):
            field_idx_diff, pos = read_uleb128(dex, pos)
            field_idx += field_idx_diff
            access_flags, pos = read_uleb128(dex, pos)
            fc, fn, ft = get_field(field_idx)
            class_info["fields"].append(f"static {fn}: {ft}")
            
        # instance fields
        field_idx = 0
        for _ in range(instance_fields_size):
            field_idx_diff, pos = read_uleb128(dex, pos)
            field_idx += field_idx_diff
            access_flags, pos = read_uleb128(dex, pos)
            fc, fn, ft = get_field(field_idx)
            class_info["fields"].append(f"{fn}: {ft}")
            
        # direct methods
        method_idx = 0
        for _ in range(direct_methods_size):
            method_idx_diff, pos = read_uleb128(dex, pos)
            method_idx += method_idx_diff
            access_flags, pos = read_uleb128(dex, pos)
            code_off, pos = read_uleb128(dex, pos)
            mc, mn = get_method(method_idx)
            code_strings = []
            if code_off > 0:
                registers_size, ins_size, outs_size, tries_size, debug_info_off, insns_size = struct.unpack_from('<HHIIII', dex, code_off)
                insns = dex[code_off+16 : code_off+16 + insns_size*2]
                ip = 0
                while ip < len(insns):
                    op = insns[ip]
                    if op == 0x1A and ip + 4 <= len(insns):
                        sidx = struct.unpack_from('<H', insns, ip + 2)[0]
                        if sidx < string_ids_size:
                            code_strings.append(get_string(sidx))
                        ip += 4
                    elif op == 0x1B and ip + 6 <= len(insns):
                        sidx = struct.unpack_from('<I', insns, ip + 2)[0]
                        if sidx < string_ids_size:
                            code_strings.append(get_string(sidx))
                        ip += 6
                    else:
                        ip += 2
            class_info["methods"].append({"type": "direct", "name": mn, "strings": list(set(code_strings))})
            
        # virtual methods
        method_idx = 0
        for _ in range(virtual_methods_size):
            method_idx_diff, pos = read_uleb128(dex, pos)
            method_idx += method_idx_diff
            access_flags, pos = read_uleb128(dex, pos)
            code_off, pos = read_uleb128(dex, pos)
            mc, mn = get_method(method_idx)
            code_strings = []
            if code_off > 0:
                registers_size, ins_size, outs_size, tries_size, debug_info_off, insns_size = struct.unpack_from('<HHIIII', dex, code_off)
                insns = dex[code_off+16 : code_off+16 + insns_size*2]
                ip = 0
                while ip < len(insns):
                    op = insns[ip]
                    if op == 0x1A and ip + 4 <= len(insns):
                        sidx = struct.unpack_from('<H', insns, ip + 2)[0]
                        if sidx < string_ids_size:
                            code_strings.append(get_string(sidx))
                        ip += 4
                    elif op == 0x1B and ip + 6 <= len(insns):
                        sidx = struct.unpack_from('<I', insns, ip + 2)[0]
                        if sidx < string_ids_size:
                            code_strings.append(get_string(sidx))
                        ip += 6
                    else:
                        ip += 2
            class_info["methods"].append({"type": "virtual", "name": mn, "strings": list(set(code_strings))})
            
    results[cname] = class_info

with open(r'c:\laragon\www\app-ios-astonCamera\scratch\target_classes_decompiled.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"SUCCESS: Saved {len(results)} target classes")
