import time, json, urllib.request, urllib.error

ENDPOINTS = [
    ("UIMode", "http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Menu.UIMode"),
    ("RecordStatus", "http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Preview.MJPEG.status.record"),
    ("filelist_xml", "http://192.72.1.1/cdv/filelist.xml"),
    ("movielist_xml", "http://192.72.1.1/cdv/movielist.xml"),
    ("photolist_xml", "http://192.72.1.1/cdv/photolist.xml")
]

def probe(label="ROUND"):
    results = {"label": label, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "endpoints": {}}
    for name, url in ENDPOINTS:
        start_t = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                status = resp.status
                headers = dict(resp.headers)
                body = resp.read()
                results["endpoints"][name] = {
                    "url": url,
                    "status": status,
                    "content_type": headers.get("Content-Type", ""),
                    "content_length": len(body),
                    "body_preview": body[:500].decode("utf-8", errors="replace")
                }
        except urllib.error.HTTPError as e:
            results["endpoints"][name] = {
                "url": url,
                "status": e.code,
                "content_type": dict(e.headers).get("Content-Type", ""),
                "content_length": len(e.read() if e.fp else b""),
                "body_preview": f"HTTP {e.code}"
            }
        except Exception as e:
            results["endpoints"][name] = {
                "url": url,
                "status": "ERROR",
                "error": str(e)
            }
        time.sleep(1.0)
    return results

if __name__ == "__main__":
    import sys
    label = sys.argv[1] if len(sys.argv) > 1 else "TEST"
    res = probe(label)
    print(json.dumps(res, indent=2, ensure_ascii=False))
