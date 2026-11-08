import time, urllib.request, json

def check_mode():
    try:
        with urllib.request.urlopen('http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Menu.UIMode', timeout=2) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
            for line in text.splitlines():
                if 'Camera.Menu.UIMode=' in line:
                    return line.split('=')[1].strip()
    except Exception as e:
        return f"ERR_{e}"
    return "UNKNOWN"

print("Starting passive check (10 samples, 2s interval)...")
for i in range(10):
    mode = check_mode()
    print(f"Sample {i+1}: UIMode={mode}")
    if mode == "PLAYBACK":
        print("PLAYBACK DETECTED!")
        break
    time.sleep(2)
