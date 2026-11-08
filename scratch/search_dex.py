import zipfile, struct, re

apk_path = r'c:\laragon\www\app-ios-astonCamera\tmcam-for-mstar-1-1-25082115.apk'

targets = [
    'DeviceApi', 'DeviceHttpEngine', 'DeviceRequest', 'FileListResponse',
    'MediaFile', 'MediaDataAccess', 'Downloader', 'getFileList', 'downloadFile',
    'Camera.Preview.Source.1.Camid', 'CamIdResponse'
]

with zipfile.ZipFile(apk_path, 'r') as z:
    for dex_name in ['classes.dex', 'classes2.dex']:
        dex_data = z.read(dex_name)
        print(f"\n=== {dex_name} (Size: {len(dex_data)} bytes) ===")
        for t in targets:
            count = len(re.findall(re.escape(t.encode()), dex_data))
            if count > 0:
                print(f"  Target '{t}': found {count} times")
