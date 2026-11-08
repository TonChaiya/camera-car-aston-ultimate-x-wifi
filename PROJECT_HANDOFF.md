# PROJECT_HANDOFF: ASTON Ultimate X WiFi 2K Custom iOS App Project

เอกสารส่งมอบงานฉบับสมบูรณ์ (Project Handoff Document) สำหรับส่งมอบงานให้ AI Agent หรือผู้พัฒนาชุดถัดไปทำงานต่อได้ทันทีโดยไม่ต้องเริ่มต้นวิเคราะห์ใหม่

---

## 1. วัตถุประสงค์โครงการ (Project Objective)

- พัฒนาแอปพลิเคชัน iOS (Swift / SwiftUI) ขึ้นมาใช้งานทดแทนแอป **Ti2Cam** อย่างสมบูรณ์
- เป็นแอปแบบ Clean & Ad-Free (ไม่มีโฆษณา ไม่แอบส่งข้อมูลออกภายนอก)
- รองรับการดูภาพสด (Live View) และการเข้าถึงไฟล์วิดีโอย้อนหลัง ทั้งจาก **กล้องหน้า (Front Camera)** และ **กล้องหลัง (Rear Camera)**
- ใช้งานผ่านการเชื่อมต่อ Wi-Fi ท้องถิ่นของตัวกล้องโดยตรง (Direct Wi-Fi / SoftAP)

---

## 2. ข้อมูลอุปกรณ์ เฟิร์มแวร์ และชิปเซ็ต (Hardware & Firmware Profile)

| รายการ | รายละเอียด | สถานะการพิสูจน์ |
|---|---|---|
| **รุ่นกล้อง (Model)** | ASTON Ultimate X WiFi 2K (Dual Dashcam) | `VERIFIED` |
| **เวอร์ชันเฟิร์มแวร์บนเครื่อง** | `K90D.20200720.V2.1` | `VERIFIED` (อ่านจาก `Camera.Menu.FWversion`) |
| **สถาปัตยกรรมชิปเซ็ต** | Alpha Imaging Technology (**AIT** / MStar AIT DVR Architecture) | `VERIFIED` |
| **Magic Header ในเฟิร์มแวร์** | `AITS` (ที่ Offset `0x00000000`), `MCR5` (ที่ Offset `0x00000020`) | `VERIFIED` |
| **Web Server Signature** | `SERVER: AIT Multimedia Network Solution, UPnP/1.0 devices/1.6.19` (Header ภายใน `X-User-Agent: redsonic`) | `VERIFIED` |
| **ไฟล์เฟิร์มแวร์ในโปรเจกต์** | `C:\laragon\www\app-ios-astonCamera\SD_CarDV.bin` | `VERIFIED` |
| **ขนาดไฟล์เฟิร์มแวร์** | 4,062,038 bytes (~3.87 MB) | `VERIFIED` |
| **SHA-256 ของ SD_CarDV.bin** | `5B18635E8BD3D6973567E15452DAE62BBDC613DC9772CA4CBDC043D3E9DDE0B9` | `VERIFIED` |

---

## 3. โครงสร้าง Workspace และตำแหน่งไฟล์สำคัญ (Workspace Structure)

Root Workspace: `C:\laragon\www\app-ios-astonCamera\`

```
C:\laragon\www\app-ios-astonCamera\
│
├── SD_CarDV.bin                            # ไฟล์ไบนารีเฟิร์มแวร์ต้นฉบับ
├── PROJECT_HANDOFF.md                      # [ไฟล์นี้] เอกสารส่งมอบงานฉบับสมบูรณ์
├── environment-check-report.md             # รายงานผลการตรวจสอบสภาพแวดล้อม (Phase 0)
├── phase1-firmware-protocol-report.md      # รายงานวิเคราะห์เฟิร์มแวร์และโพรโทคอล (Phase 1)
├── phase2-stream-validation-report.md      # รายงานทดสอบสตรีม RTSP ทางเน็ตเวิร์ก (Phase 2)
├── phase2b-visual-stream-report.md         # รายงานติดตั้ง FFmpeg และถอดรหัสภาพจริง (Phase 2B)
│
├── artifacts\
│   └── stream-verification\               # โฟลเดอร์เก็บภาพนิ่งตัวอย่างที่จับจากสตรีมจริง
│       ├── frame_v1.jpg                    # ภาพจาก rtsp://192.72.1.1/liveRTSP/v1 (H.264)
│       ├── frame_av1.jpg                   # ภาพจาก rtsp://192.72.1.1/liveRTSP/av1 (MJPEG)
│       ├── frame_av2.jpg                   # ภาพจาก rtsp://192.72.1.1/liveRTSP/av2 (H.264)
│       └── frame_v2.jpg                    # ภาพจาก rtsp://192.72.1.1/liveRTSP/v2 (MJPEG)
│
└── tools\
    └── ffmpeg\                             # FFmpeg Portable ที่ติดตั้งเฉพาะใน Workspace
        └── bin\
            ├── ffmpeg.exe                  # ตัวถอดรหัส/แปลงสัญญาณ (version 9.0.2)
            └── ffprobe.exe                 # ตัววิเคราะห์สตรีมและคอนเทนเนอร์
```

---

## 4. การตั้งค่าเครือข่าย Dual Wi-Fi บน Windows (Network Topology)

ระบบทำงานบนโครงสร้าง **Dual Wi-Fi** พร้อมกัน เพื่อให้สามารถเชื่อมต่อกล้องและอินเทอร์เน็ตได้พร้อมกันโดยไม่หลุด:

```
[ Windows PC ]
   ├── Wi-Fi (Intel Dual Band Wireless-AC 3160)
   │     └── IP: 192.168.1.99 -> SSID: RPST_Korsariem_5GHz (🌐 อินเทอร์เน็ต)
   │
   └── Wi-Fi 2 (TP-Link Wireless Nano USB Adapter)
         └── IP: 192.72.1.101 -> SSID: WK_CarDV_WiFi_7277 (📷 กล้อง ASTON IP 192.72.1.1)
```

- **IP กล้อง (Camera Gateway):** `192.72.1.1`
- **พอร์ตที่เปิดให้บริการบนกล้อง:**
  - พอร์ต 80: HTTP Web / CGI Server (`OPEN`)
  - พอร์ต 554: RTSP Streaming Server (`OPEN`)
  - พอร์ต 8554, 8080, 8888: (`CLOSED`)

---

## 5. สรุปผลการตรวจสอบ HTTP API บนพอร์ต 80 (HTTP API Discovery)

| Method | URL / Endpoint | พารามิเตอร์ | ผลลัพธ์ / ข้อมูลที่ตอบกลับ | สถานะ |
|---|---|---|---|---|
| `GET` | `/cgi-bin/Config.cgi` | `action=get&property=Camera.*` | คืนค่า Tree สถานะกล้องทั้งหมด (`FWversion`, `Battery`, `Menu.*`, `Preview.*`, `Record.*`) | `VERIFIED` |
| `GET` | `/cgi-bin/Config.cgi` | `action=get&property=Camera.Preview.*` | คืนค่า `H264.w=640`, `H264.h=480`, `MJPEG.fps=20`, `Source.Totals=2` | `VERIFIED` |
| `GET` | `/cgi-bin/Config.cgi` | `action=get&property=Camera.File.*` | คืนค่า `Camera.File.Total=11` (หรือ 12) แสดงจำนวนคลิปบน SD Card | `VERIFIED` |
| `GET` | `/cgi-bin/Config.cgi` | `action=get&property=Camera.DBFileNum` | คืนค่า `Camera.DBFileNum=24+127` | `VERIFIED` |
| `GET` | `/cgi-bin/Config.cgi` | `action=get&property=Camera.Record.*` | คืนค่า `Camera.Record.Remaining=420`, `Total=19991` | `VERIFIED` |
| `GET` | `/settings.html` | - | หน้า Web UI สำหรับลิงก์ไปเมนูตั้งค่า (`Status 200`) | `VERIFIED` |
| `GET` | `/MenuSettings.html`| - | หน้า Web UI สำหรับปรับค่าความละเอียดภาพ/วิดีโอ (`Status 200`) | `VERIFIED` |
| `GET` | `/simple.html` | - | หน้า Web UI สำหรับดูค่า Wi-Fi AP (เข้ารหัสแบบ UTF-16BE) | `VERIFIED` |
| `GET` | `/mj4.html` | - | หน้า Web UI พรีวิว MJPEG PUSH mode ดั้งเดิมของ AIT (`Status 200`) | `VERIFIED` |
| `GET` | `/AITlogo.jpg` | - | โลโก้ Alpha Imaging Technology บนเว็บเซิร์ฟเวอร์ (`Status 200`) | `VERIFIED` |
| `GET` | `/cgi-bin/liveMJPEG` | - | ตอบกลับ **404 Not Found** (ต้องอาศัยคำสั่งเปิดเซสชันเฉพาะ) | `VERIFIED` |
| `GET` | `/SD/`, `/DCIM/` | - | ตอบกลับ **404 Not Found** (กล้องปิด HTTP Directory Browsing) | `VERIFIED` |

> **ข้อจำกัดของ HTTP API:** หากส่งคำขอที่ Property ไม่มีอยู่ กล้องจะตอบกลับ `703 Unknown CGI-PARAM` หรือในบางกรณีส่ง 404 ซึ่งอาจทำให้เธรด CGI พักการทำงานชั่วคราว จึงต้องจำกัดคำขอไม่เกิน 1 ครั้งต่อวินาที

---

## 6. สรุปผลการตรวจสอบ RTSP Streams ทั้ง 4 เส้นทาง (RTSP Results)

ทดสอบส่งคำสั่ง `OPTIONS` -> `DESCRIBE` -> `SETUP` -> `PLAY` -> `TEARDOWN` ผ่าน RTSP over TCP บนพอร์ต 554:

| RTSP URL | วิดีโอโคเดก (Video) | เสียง (Audio) | ความละเอียด / FPS | ผลการสตรีมจริง (Throughput) |
|---|---|---|---|---|
| **`rtsp://192.72.1.1/liveRTSP/v1`** | **H.264 Main Profile** (NAL 7, 8, 28) | ไม่มี (Video Only) | 640x480 @ 29.97 fps | ✅ 137 Packets (173 KB) ใน 2.5 วินาที (~554 kbps) |
| **`rtsp://192.72.1.1/liveRTSP/av1`** | **MJPEG Baseline** (RTP PT 26) | AAC Stereo 16kHz | 640x480 @ 20 fps | ✅ 28 Packets (206 KB) ใน 2.5 วินาที (~660 kbps) |
| **`rtsp://192.72.1.1/liveRTSP/av2`** | **H.264 Main Profile** (NAL 7, 8, 28) | AAC Stereo 16kHz | 640x480 @ 29.97 fps | ✅ 227 Packets (293 KB) ใน 2.0 วินาที (~1.17 Mbps) |
| **`rtsp://192.72.1.1/liveRTSP/v2`** | **MJPEG Baseline** (RTP PT 26) | ไม่มี (Video Only) | 640x480 @ 20 fps | ✅ 77 Packets (550 KB) ใน 2.0 วินาที (~2.2 Mbps) |

---

## 7. ผลการวิเคราะห์ไฟล์ภาพทั้ง 4 ภาพ และข้อสรุปเรื่องกล้องหลัง (Visual Analysis & Crucial Correction)

### ⚠️ ข้อสรุปเดิมที่เคยผิดพลาดและได้รับการแก้ไขแล้ว (Corrected Conclusion):
- ใน Phase 1 และ Phase 2 มีข้อสมมติฐานว่า `liveRTSP/av2` และ `liveRTSP/v2` คือ **สตรีมของกล้องหลัง (Rear Camera)** เนื่องจากเฟิร์มแวร์ระบุ `Camera.Preview.Source.Totals=2` และพบเซนเซอร์ `[SENSOR1]`
- **ความจริงจากการถอดรหัสภาพจริง (Phase 2B):**
  - เมื่อนำไฟล์ภาพทั้ง 4 ภาพ (`frame_v1.jpg`, `frame_av1.jpg`, `frame_av2.jpg`, `frame_v2.jpg`) มาเปรียบเทียบพิกเซลและระดับสัญญาณ (SSIM / Luminance YAVG)
  - **พบว่าภาพทั้ง 4 ภาพเป็นมุมมองภาพเดียวกันทั้งหมด 100% (เป็นภาพจากเลนส์กล้องหน้า)**
  - ความแตกต่างของภาพเกิดจากลักษณะการบีบอัดของโคเดก (H.264 vs MJPEG) เท่านั้น ไม่ได้มาจากเลนส์คนละตัว
- **ข้อสรุป ณ ปัจจุบัน:**
  - สตรีม `liveRTSP/v1`, `av1`, `av2`, `v2` ล้วนเป็นสตรีมของ **กล้องหน้า** ในรูปแบบความละเอียดและแทร็กเสียงต่างกัน
  - **ยังไม่พบ RTSP URL สตรีมสดสำหรับกล้องหลังบนพอร์ต 554** (`NOT_FOUND / UNCONFIRMED`)

---

## 8. ข้อมูลยืนยันจากผู้ใช้เกี่ยวกับกล้องหลัง (User Confirmed Facts)

- **`USER_CONFIRMED`:** ผู้ใช้ยืนยันว่า กล้องหลังมีการติดตั้งและใช้งานได้จริง
- **`USER_CONFIRMED`:** เมื่อเปิดใช้งานผ่านแอป **Ti2Cam** จะสามารถเปิดดูวิดีโอที่บันทึกไว้จากการ์ด SD ได้ทั้งของ **กล้องหน้า** และ **กล้องหลัง** โดยไฟล์วิดีโอของกล้องหน้าและกล้องหลังถูกบันทึกแยกเป็นคนละไฟล์กัน
- กล้องหลังบันทึกภาพลง SD Card แน่นอน แต่ยังต้องค้นหาวิธีเข้าถึงภาพสด (หากมี) และวิธีดึงไฟล์วิดีโอกล้องหลังจากตัวกล้อง

---

## 9. เครื่องมือและ Dependencies ในระบบ (Installed Tools)

| เครื่องมือ | เวอร์ชัน | ตำแหน่งที่ติดตั้ง | หมายเหตุ |
|---|---|---|---|
| **PowerShell** | 5.1.19041.6456 | ในระบบ Windows | พร้อมใช้งาน |
| **Python** | 3.14.6 | `C:\Users\Mainam8888\AppData\Local\Python\pythoncore-3.14-64\python.exe` | มีโมดูลมาตรฐานเครือข่าย (`socket`, `struct`, `urllib`) |
| **FFmpeg Portable** | 9.0.2-essentials | `C:\laragon\www\app-ios-astonCamera\tools\ffmpeg\bin\ffmpeg.exe` | ติดตั้งเฉพาะใน Workspace ตรวจสอบ SHA-256 แล้ว |
| **ffprobe Portable** | 9.0.2-essentials | `C:\laragon\www\app-ios-astonCamera\tools\ffmpeg\bin\ffprobe.exe` | ติดตั้งเฉพาะใน Workspace |
| **VLC** | - | *ไม่ได้ติดตั้ง* | ไม่จำเป็นต้องติดตั้ง (ใช้ FFmpeg แทนแล้ว) |

---

## 10. สถานะความพร้อมและข้อสรุปการพิสูจน์ (Status Breakdown)

### ก. สิ่งที่ทำสำเร็จแล้ว (VERIFIED):
1. ยืนยันสถาปัตยกรรม AIT DVR ของกล้อง ASTON Ultimate X WiFi 2K
2. ถอดรหัสโครงสร้างไฟล์เฟิร์มแวร์ `SD_CarDV.bin` และพบรหัส Asset หน้าเว็บที่ซ่อนอยู่ทั้งหมด
3. ดึงค่าสถานะกล้องผ่าน `GET /cgi-bin/Config.cgi?action=get&property=Camera.*` สำเร็จ
4. ดึงสตรีมภาพสด RTSP กล้องหน้าได้สำเร็จ 100% ทั้ง H.264 (Main Profile 640x480 @ 30fps) และ MJPEG โดยไม่ต้องใช้ Ti2Cam
5. ติดตั้ง FFmpeg Portable ที่ผ่านการตรวจสอบ Checksum และถอดรหัสภาพนิ่งตัวอย่างได้สำเร็จทั้ง 4 สตรีม

### ข. สิ่งที่ยังไม่สำเร็จและต้องค้นหาต่อ (PENDING / NOT_TESTED):
1. **ยังไม่พบเส้นทางดึงสตรีมสด (Live RTSP) ของกล้องหลัง:** ต้องหาว่ากล้องหลังใช้ URL อื่น (เช่น `/liveRTSP/v3`, `/liveRTSP/rear`, พอร์ตอื่น หรือต้องส่ง CGI Parameter เพื่อสลับ Source)
2. **Recorded Video API (การดึงรายการไฟล์ย้อนหลัง):** ยังไม่ทราบรูปแบบคำสั่งอ่านรายการไฟล์วิดีโอ MP4 บน SD Card จากกล้อง
3. **การแยกแยะไฟล์กล้องหน้า–หลัง (Front/Rear File Naming):** ยังไม่ทราบรูปแบบการตั้งชื่อไฟล์ของกล้องหน้าและกล้องหลัง (เช่น `...A.mp4` / `...B.mp4` หรือแยกโฟลเดอร์ `Normal/` vs `Event/`)

---

## 11. ข้อจำกัดและคำสั่งต้องห้าม (Strict Safety Rules)

เพื่อป้องกันการเปลี่ยนค่าคอนฟิกกล้อง การหยุดบันทึก หรือความเสียหายต่อเฟิร์มแวร์และข้อมูลใน SD Card:

> [!CAUTION]
> **คำสั่งต้องห้ามเด็ดขาด (Strictly Forbidden Actions):**
> 1. **ห้าม Flash หรือ Update Firmware เด็ดขาด**
> 2. **ห้ามใช้คำสั่ง `Config.cgi` ที่มี `action=set`, `delete`, `reset` หรือ `format`**
> 3. **ห้ามสั่งหยุดหรือเริ่มการบันทึกวิดีโอของกล้อง**
> 4. **ห้ามสั่งลบ ย้าย หรือเขียนทับไฟล์ใด ๆ บนกล้องหรือการ์ด SD**
> 5. **ห้ามแก้ไข Network Routing, Adapter Settings หรือ Registry ของ Windows**
> 6. **ห้าม Fuzzing หรือ Port Scanning สุ่มสี่สุ่มห้า**
> 7. **จำกัดคำขอ HTTP ไม่เกิน 1 ครั้งต่อวินาที** และ Timeout ไม่เกิน 3 วินาที
> 8. **ห้ามเชื่อมต่อ RTSP แช่ทิ้งไว้นาน** และต้องส่ง `TEARDOWN` ทุกครั้งเมื่อเสร็จงานเพื่อคืนทรัพยากร Socket ให้กล้อง

---

## 12. แผนงานขั้นถัดไป (Next Steps for Next Agent)

1. **สืบค้น Recorded Video API (Phase 3):**
   - วิเคราะห์เฟิร์มแวร์ `SD_CarDV.bin` ในส่วนที่เกี่ยวข้องกับการจัดการไฟล์และฐานข้อมูล SQLite/FAT
   - ค้นหาวิธีอ่านรายการไฟล์ เช่น `action=dir`, `action=list`, หรือคิวรีคุณสมบัติ `Camera.File.*` แบบระบุโฟลเดอร์
   - ศึกษารูปแบบชื่อไฟล์และตำแหน่งโฟลเดอร์สำหรับกล้องหน้าและกล้องหลัง
2. **สืบค้นการเข้าถึงภาพสดกล้องหลัง (Rear Camera Live Stream Discovery):**
   - ตรวจสอบว่าแอป Ti2Cam ดึงภาพสดกล้องหลังได้หรือไม่ หรือใช้การดึงไฟล์คลิปสั้นมาแสดง
   - ตรวจสอบคำสั่งสลับการแสดงผลภาพสดของ AIT เช่น `property=Camera.Preview.Source.Select` แบบ Read-only query
3. **พัฒนาแอป iOS (SwiftUI + AVFoundation / VideoToolbox):**
   - เริ่มสร้างโครงร่างโปรเจกต์ Xcode (SwiftUI)
   - เชื่อมต่อ RTSP กล้องหน้าผ่าน `rtsp://192.72.1.1/liveRTSP/v1`

---

## 13. คำสั่งสำหรับ AI Agent ตัวใหม่ (Prompt for New AI Agent)

คัดลอกข้อความด้านล่างนี้เพื่อสั่งงาน AI Agent ตัวถัดไป:

```markdown
คุณกำลังทำงานในโปรเจกต์ app-ios-astonCamera บนกล้อง ASTON Ultimate X WiFi 2K
กรุณาอ่านข้อมูลสรุปสถานะล่าสุดจากไฟล์ `PROJECT_HANDOFF.md` ที่ Root ของ Workspace ให้ครบถ้วนก่อนเริ่มงาน

ข้อเท็จจริงสำคัญที่ได้รับการพิสูจน์แล้ว:
1. การเชื่อมต่อ Dual Wi-Fi และเครือข่ายกล้อง 192.72.1.1 ทำงานพร้อมใช้งาน
2. สตรีมภาพสดกล้องหน้าผ่าน RTSP (rtsp://192.72.1.1/liveRTSP/v1) เป็น H.264 640x480 @ 30fps ยืนยันทำงานได้จริง 100%
3. สตรีมทั้ง 4 เส้นทาง (v1, av1, av2, v2) เป็นภาพจากกล้องหน้าทั้งหมด ยังไม่พบ RTSP ของกล้องหลัง
4. ผู้ใช้ยืนยันว่าในแอป Ti2Cam มีวิดีโอบันทึกของทั้งกล้องหน้าและกล้องหลังแยกไฟล์กันในการ์ด SD
5. มีเครื่องมือ FFmpeg Portable ติดตั้งอยู่ที่ tools/ffmpeg/bin/ffmpeg.exe พร้อมใช้งาน

ภารกิจของคุณ:
ดำเนินการ Phase 3: ค้นหา Recorded Video API (รูปแบบการแสดงรายการไฟล์วิดีโอบน SD Card) และหาวิธีระบุไฟล์กล้องหน้าและกล้องหลัง รวมถึงสืบค้นช่องทางภาพสดของกล้องหลัง
ปฏิบัติตาม Safety Rules ใน PROJECT_HANDOFF.md เคร่งครัด (Read-only เท่านั้น ห้าม action=set หรือ format)
```
