# PHASE 3H — Rear Camera Video Download & Verification

## VERIFIED_FROM_LIVE_CAMERA

### 1) Camera connectivity and recording status
- Camera IP: `192.72.1.1`
- Status endpoint used: `http://192.72.1.1/cgi-bin/Config.cgi?action=get&property=Camera.Preview.MJPEG.status.record`
- Live result observed: `0 OK Camera.Preview.MJPEG.status.record=Recording`
- Conclusion: camera was reachable and recording state was confirmed before the rear-file read.

### 2) Rear file list confirmation
- Rear XML endpoint used: `http://192.72.1.1/cgi-bin/Config.cgi?action=reardir&property=Normal&format=all&count=999&from=0&backward=`
- Live XML included the exact target rear file:
  - `/SD/Normal/R/FILE261108-112713-068376R.TS`
- The XML also showed the size for that file as:
  - `148701184` bytes
- Conclusion: the exact rear file existed in the live file list and had a non-zero size.

### 3) APK code evidence for how this file is accessed
Relevant decompiled code:
- [sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java](sources/com/tima/app/common/devices/mstar/device/beans/FileListResponse.java#L16-L55)
- [sources/com/tima/app/common/devices/mstar/device/beans/MediaFile.java](sources/com/tima/app/common/devices/mstar/device/beans/MediaFile.java#L7-L40)
- [sources/com/tima/app/common/medialist/dao/Downloader.java](sources/com/tima/app/common/medialist/dao/Downloader.java#L49-L116)

The code establishes:
- `mediaFile.url = DeviceKit.getHttpPrefix() + strFirstElementTextByTag;`
- the remote clip URL is built directly from the XML `<name>` field
- the downloader uses HTTP `GET`
- when a local cache exists, it sends `Range: bytes=<offset>-`
- the client handles both `200 OK` and `206 Partial Content`

### 4) Exact rear file URL used
- `http://192.72.1.1/SD/Normal/R/FILE261108-112713-068376R.TS`

This URL matches the live XML entry exactly and is the only rear clip targeted in this phase.

## UNVERIFIED

### 1) Actual rear video download result
The explicit file download was not completed in this session.

Reasons:
- the safe verification requirement was to read only a constrained range and stop if abnormal
- the live Range-response behavior for this exact URL remains unconfirmed by a successful partial read
- no real full-file download or ffprobe validation was performed in this phase

### 2) HTTP Range support on the exact rear file
The APK code strongly suggests the client expects Range support, but the actual server behavior for the rear TS file is still unverified in live capture.

The live evidence is:
- XML confirms the file exists and has non-zero size
- code confirms the app calls `Range: bytes=<offset>-` when resuming
- live `Range: bytes=0-4095` response was not captured successfully in this environment

Therefore:
- `RANGE_SUPPORTED`: UNVERIFIED
- `RANGE_IGNORED`: UNVERIFIED
- `UNKNOWN`: CONFIRMED as the current live status for the exact rear file partial-read step

### 3) FFprobe / codec / resolution / FPS / duration
These values remain unverified because no actual rear video data was downloaded or decoded in this phase.

## SAFETY STATUS

No unsafe operations were performed:
- no `action=set`
- no delete / format / reset
- no UI mode change
- no recording stop
- no SD-card modification
- no firmware flash
- no extra endpoint probing beyond the confirmed XML and status APIs
- no full video download

## FINAL CONCLUSION

สิ่งที่ยืนยันได้จริงจากการตรวจสอบมีเพียง 3 อย่างหลัก:
1. กล้องยังตอบสนองต่อ API วัดสถานะ `Recording` ได้จริง
2. ไฟล์ rear ที่ต้องการมีอยู่ใน XML กล้องหลัง และมีขนาด `148701184` bytes
3. โค้ด APK ยืนยันแอปจะเรียกไฟล์นี้ผ่าน HTTP GET และรองรับการอ่านแบบ partial-range ในทางทฤษฎี

สิ่งที่ยังยืนยันไม่ได้จริงใน Phase นี้:
- การตอบกลับ `Range: bytes=0-4095` จากเซิร์ฟเวอร์กล้องหลัง
- การดาวน์โหลดเต็มวิดีโอ rear
- Codec, Resolution, FPS, Duration, Audio Codec และ FFmpeg decode result

รายงานนี้จึงถูกจัดทำตามหลักฐานที่ตรวจสอบได้จริงเท่านั้น และหยุดทันทีเมื่อพบว่าข้อมูลที่ต้องการยังไม่สามารถพิสูจน์ได้แบบ live read-only ในสภาพแวดล้อมนี้
