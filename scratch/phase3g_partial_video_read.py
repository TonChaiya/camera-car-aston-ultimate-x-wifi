#!/usr/bin/env python3
import binascii
import json
import time
from urllib import request, error

STATUS_URL = 'http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Preview.MJPEG.status.record'
FRONT_URL = 'http://192.72.1.1/SD/Normal/F/FILE261108-112713-068376F.TS'
REAR_URL = 'http://192.72.1.1/SD/Normal/R/FILE261108-112713-068376R.TS'
MAX_BYTES = 4096
TIMEOUT = 3


def status_get(url):
    req = request.Request(url, method='GET')
    try:
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(256)
            return {
                'http_status': resp.status,
                'status_line': getattr(resp, 'status', None),
                'body': body.decode('utf-8', 'replace'),
                'headers': dict(resp.headers.items()),
            }
    except error.HTTPError as e:
        body = e.read(256)
        return {
            'http_status': e.code,
            'status_line': e.code,
            'body': body.decode('utf-8', 'replace'),
            'headers': dict(e.headers.items()),
        }
    except Exception as e:
        return {
            'http_status': 'EXCEPTION',
            'status_line': 'EXCEPTION',
            'body': type(e).__name__ + ': ' + str(e),
            'headers': {},
        }


def partial_get(url):
    req = request.Request(url, headers={'Range': 'bytes=0-4095'}, method='GET')
    try:
        with request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read(MAX_BYTES)
            body_prefix = raw[:32]
            hex_prefix = binascii.hexlify(body_prefix).decode('ascii').upper()
            return {
                'http_status': resp.status,
                'status_line': getattr(resp, 'status', None),
                'content_type': resp.headers.get('Content-Type', ''),
                'content_length': resp.headers.get('Content-Length', ''),
                'content_range': resp.headers.get('Content-Range', ''),
                'accept_ranges': resp.headers.get('Accept-Ranges', ''),
                'range_result': 'RANGE_SUPPORTED' if resp.status == 206 else ('RANGE_IGNORED' if resp.status == 200 else 'UNKNOWN'),
                'prefix_len': len(body_prefix),
                'hex_prefix': hex_prefix,
                'body_preview': body_prefix[:32],
            }
    except error.HTTPError as e:
        body = e.read(MAX_BYTES)
        hex_prefix = binascii.hexlify(body[:32]).decode('ascii').upper()
        return {
            'http_status': e.code,
            'status_line': e.code,
            'content_type': e.headers.get('Content-Type', ''),
            'content_length': e.headers.get('Content-Length', ''),
            'content_range': e.headers.get('Content-Range', ''),
            'accept_ranges': e.headers.get('Accept-Ranges', ''),
            'range_result': 'UNKNOWN',
            'prefix_len': len(body[:32]),
            'hex_prefix': hex_prefix,
            'body_preview': body[:32],
        }
    except Exception as e:
        return {
            'http_status': 'EXCEPTION',
            'status_line': 'EXCEPTION',
            'content_type': '',
            'content_length': '',
            'content_range': '',
            'accept_ranges': '',
            'range_result': 'UNKNOWN',
            'prefix_len': 0,
            'hex_prefix': '',
            'body_preview': b'',
            'error': type(e).__name__ + ': ' + str(e),
        }


def build_report(results):
    front = results['front']
    rear = results['rear']
    status_before = results['status_before']
    status_after = results['status_after']

    def section(title):
        return f'## {title}\n\n'

    lines = []
    lines.append('# PHASE 3G — Safe Front/Rear Video Partial Read Verification')
    lines.append('')
    lines.append(section('VERIFIED_FROM_LIVE_CAMERA'))
    lines.append(f'- Recording status before: {status_before["http_status"]} / {status_before["body"].strip()}')
    lines.append(f'- Recording status after: {status_after["http_status"]} / {status_after["body"].strip()}')
    lines.append(f'- Selected front file: {FRONT_URL}')
    lines.append(f'- Selected rear file: {REAR_URL}')
    lines.append('')
    lines.append(section('RANGE_SUPPORTED / RANGE_IGNORED / UNKNOWN'))
    lines.append(f'- Front: {front["range_result"]} | HTTP {front["http_status"]} | Content-Range: {front["content_range"] or "-"} | Accept-Ranges: {front["accept_ranges"] or "-"}')
    lines.append(f'- Rear: {rear["range_result"]} | HTTP {rear["http_status"]} | Content-Range: {rear["content_range"] or "-"} | Accept-Ranges: {rear["accept_ranges"] or "-"}')
    lines.append('')
    lines.append(section('FILE_CONTENT_PREFIX'))
    lines.append(f'- Front prefix length: {front["prefix_len"]} bytes')
    lines.append(f'- Front hex prefix: {front["hex_prefix"]}')
    lines.append(f'- Rear prefix length: {rear["prefix_len"]} bytes')
    lines.append(f'- Rear hex prefix: {rear["hex_prefix"]}')
    lines.append('')
    lines.append(section('FRONT / REAR RESULT'))
    lines.append(f'- FRONT HTTP: {front["http_status"]}')
    lines.append(f'- FRONT Content-Type: {front["content_type"] or "-"}')
    lines.append(f'- FRONT Content-Length: {front["content_length"] or "-"}')
    lines.append(f'- FRONT Content-Range: {front["content_range"] or "-"}')
    lines.append(f'- FRONT Accept-Ranges: {front["accept_ranges"] or "-"}')
    lines.append('')
    lines.append(f'- REAR HTTP: {rear["http_status"]}')
    lines.append(f'- REAR Content-Type: {rear["content_type"] or "-"}')
    lines.append(f'- REAR Content-Length: {rear["content_length"] or "-"}')
    lines.append(f'- REAR Content-Range: {rear["content_range"] or "-"}')
    lines.append(f'- REAR Accept-Ranges: {rear["accept_ranges"] or "-"}')
    lines.append('')
    lines.append(section('NEXT_SAFE_STEP'))
    lines.append('- Use one front and one rear non-zero-size file with matching timestamp and serial suffix.')
    lines.append('- Repeat only the same Range: bytes=0-4095 GET on the exact file URLs, while reading no more than 4096 bytes each time.')
    lines.append('- If the server returns 206 with Content-Range, treat the camera as Range-supported for partial reads.')
    lines.append('- If it returns 200 only, record Range as ignored and stop without attempting other endpoints.')
    lines.append('- No video download, no SD-card editing, and no state-changing commands.')
    return '\n'.join(lines) + '\n'


def main():
    print('PHASE 3G START')
    status_before = status_get(STATUS_URL)
    print('STATUS_BEFORE', json.dumps(status_before, ensure_ascii=False))
    if status_before.get('http_status') in ('EXCEPTION', 'ERROR'):
        print('ABNORMAL: status probe failed; stopping before file reads.')
        return

    time.sleep(1)
    front = partial_get(FRONT_URL)
    print('FRONT', json.dumps(front, ensure_ascii=False))
    if front.get('http_status') in ('EXCEPTION',) or front.get('http_status') not in (200, 206):
        print('ABNORMAL: front partial read failed; stopping.')
        status_after = status_get(STATUS_URL)
        print('STATUS_AFTER', json.dumps(status_after, ensure_ascii=False))
        return

    time.sleep(1)
    rear = partial_get(REAR_URL)
    print('REAR', json.dumps(rear, ensure_ascii=False))
    if rear.get('http_status') in ('EXCEPTION',) or rear.get('http_status') not in (200, 206):
        print('ABNORMAL: rear partial read failed; stopping.')
        status_after = status_get(STATUS_URL)
        print('STATUS_AFTER', json.dumps(status_after, ensure_ascii=False))
        return

    status_after = status_get(STATUS_URL)
    print('STATUS_AFTER', json.dumps(status_after, ensure_ascii=False))

    report = build_report({
        'status_before': status_before,
        'status_after': status_after,
        'front': front,
        'rear': rear,
    })
    print('\nREPORT_START\n')
    print(report)
    print('\nREPORT_END\n')

    with open('phase3g-partial-video-read.md', 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == '__main__':
    main()
