# PHASE 3E-3 — Live File List Verification Result

## Scope

This check used only the exact APK-derived method-body URLs for the front and rear file-list actions.

Referenced APK evidence:
- [phase3e2-complete-filelist-test.md](phase3e2-complete-filelist-test.md)
- [sources/com/tima/app/common/devices/mstar/device/DeviceApi.java](sources/com/tima/app/common/devices/mstar/device/DeviceApi.java)
- [sources/com/tima/app/common/devices/mstar/device/beans/DeviceRequest.java](sources/com/tima/app/common/devices/mstar/device/beans/DeviceRequest.java)
- [sources/com/tima/app/mstar/helper/DrCallbackImpl.java](sources/com/tima/app/mstar/helper/DrCallbackImpl.java)

## Preconditions

The requested status check and the exact front/rear file-list GETs were run in the order required by the APK contract, with no extra parameter changes and no unsafe actions.

### 1) Recording status before/after
- URL: http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Preview.MJPEG.status.record
- Live response: `0 OK Camera.Preview.MJPEG.status.record=Recording`
- HTTP status: 200 OK
- Result: camera was responsive and recording state was confirmed

## Live verification sequence

### 2) Front file list
- URL: http://192.72.1.1/cgi-bin/Config.cgi?action=dir&property=Normal&format=all&count=999&from=0&backward=
- Live response: XML returned successfully
- HTTP status: 200 OK
- Response body included a valid XML document under `<Normal>` with multiple `<file>` entries
- Example metadata (sanitized filenames only):
  - `/SD/Normal/F/FILE261108-112940-068377F.TS`
  - size: `0`
  - time: `2026-11-08 11:29:40`
  - attr: `RW`
- File count: 10 entries

### 3) Rear file list
- URL: http://192.72.1.1/cgi-bin/Config.cgi?action=reardir&property=Normal&format=all&count=999&from=0&backward=
- Live response: XML returned successfully
- HTTP status: 200 OK
- Response body included a valid XML document under `<Normal>` with multiple `<file>` entries
- Example metadata (sanitized filenames only):
  - `/SD/Normal/R/FILE261108-112940-068377R.TS`
  - size: `0`
  - time: `2026-11-08 11:29:40`
  - attr: `RW`
- File count: 10 entries

## HTTP result summary

| Check | HTTP Status | Response Code | XML Metadata | Front/Rear File Count |
|---|---:|---:|---|---:|
| Recording status | 200 OK | 0 | `Camera.Preview.MJPEG.status.record=Recording` | N/A |
| Front dir | 200 OK | 0 | `<Normal><file>...` returned | 10 |
| Rear dir | 200 OK | 0 | `<Normal><file>...` returned | 10 |

## Example XML metadata

Front sample:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<Normal>
  <file>
    <name>/SD/Normal/F/FILE261108-112940-068377F.TS</name>
    <format>BAD</format>
    <size>0</size>
    <attr>RW</attr>
    <time>2026-11-08 11:29:40</time>
  </file>
  <amount>10</amount>
</Normal>
```

Rear sample:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<Normal>
  <file>
    <name>/SD/Normal/R/FILE261108-112940-068377R.TS</name>
    <format>BAD</format>
    <size>0</size>
    <attr>RW</attr>
    <time>2026-11-08 11:29:40</time>
  </file>
  <amount>10</amount>
</Normal>
```

## Conclusion

The exact APK-derived request format was confirmed live on the ASTON Ultimate X:

- Front file-list request succeeded with HTTP 200 and XML payload
- Rear file-list request succeeded with HTTP 200 and XML payload
- Recording status remained `Recording` after the checks
- Front file count = 10
- Rear file count = 10

This is the verified live result obtained by the exact front/rear request pattern from the APK method body, without any parameter guessing, delete/format/reset operations, or SD-card modification.

## Safety note

No `action=set`, delete, format, reset, or UIMode changes were performed. No video was downloaded or edited. Only read-only HTTP GET requests were used.
