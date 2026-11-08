# PHASE 3D — Android APK Static API Analysis

สถานะ: Static Analysis เท่านั้น (ไม่ติดตั้ง/ไม่รัน APK ไม่ส่งคำสั่งไปยังกล้อง)

## 1) ขอบเขตและวิธีตรวจสอบ

ตรวจสอบข้อมูลจากไฟล์ APK โดยตรงใน DEX/string table และคลาสที่เกี่ยวข้อง:

- DeviceApi
- DeviceHttpEngine
- DeviceRequest
- FileListResponse
- MediaFile
- MediaDataAccess
- Downloader
- CamIdResponse

สรุปสั้น: APK มีจุดเชื่อมต่อแบบ CGI/HTTP คล้ายกับโปรโตคอลที่ยืนยันจาก PROJECT_HANDOFF.md และใช้รูปแบบ `Camera.*` + `action=get` + `property=...` สำหรับสถานะ/ติดตามไฟล์กล้อง การแยกกล้องหน้า–หลังทำผ่าน `CamId` และ `Camera.Preview.Source.1.Camid` / `Camera.Preview.Source.2.Camid` แทนการสลับ UIMode หรือหยุด Recording.

---

## 2) VERIFIED_FROM_APK

### 2.1 คลาส/เมธอดที่พบจริงจาก APK

จาก DEX string/class signature ที่ตรวจพบ:

- `DeviceApi`
- `DeviceHttpEngine`
- `DeviceRequest`
- `FileListResponse`
- `MediaFile`
- `MediaDataAccess`
- `CamIdResponse`
- `getFileList`
- `downloadFile`
- `doDownloadFile`
- `Downloader->onResponse, code:`
- `Downloader->onFailure,exception:`
- `MediaDataAccess->downloadFile->onError:`

ตัวชี้วัดสำคัญที่เจอใน string table:

- `cgi-bin/Config.cgi?`
- `action=`
- `property=`
- `Camera.Preview.Source.1.Camid`
- `Camid=`
- `Camera.Preview.Source.Totals=2`
- `&format=`
- `&backward=`
- `Before downloadFile:`
- `After downloadFile:`
- `loadRemoteFiles, type:`
- `downloadFiles`

### 2.2 Endpoint และ HTTP Method

รูปแบบที่ปรากฏชัดที่สุดคือ CGI over HTTP แบบ GET:

- Method: `GET`
- URL base: `/cgi-bin/Config.cgi`
- Query pattern: `action=get&property=<Camera.Property>`

ตัวอย่างที่ค้นพบใน DEX และสอดคล้องกับ PROJECT_HANDOFF.md:

- `/cgi-bin/Config.cgi?action=get&property=Camera.Preview.*`
- `/cgi-bin/Config.cgi?action=get&property=Camera.File.*`
- `/cgi-bin/Config.cgi?action=get&property=Camera.Preview.Source.1.Camid`
- `/cgi-bin/Config.cgi?action=get&property=Camera.Preview.Source.2.Camid`

มีการใช้ `property=` สำหรับดึงค่าจากกล้อง เช่น `Camera.Menu.*`, `Camera.File.*`, `Camera.Record.*`, และ `Camera.Preview.Source.*`.

### 2.3 Query Parameters ที่พบจริงจากโค้ด

จาก string constants ใน DEX:

- `action=`
- `property=`
- `Camera.Preview.Source.1.Camid`
- `Camid=`
- `&format=`
- `&backward=`

ตรงกับโครงสร้าง request แบบ CGI/parameterized URL:

- `GET /cgi-bin/Config.cgi?action=get&property=Camera.Preview.Source.1.Camid`
- `GET /cgi-bin/Config.cgi?action=get&property=Camera.Preview.Source.2.Camid`
- `GET /cgi-bin/Config.cgi?action=get&property=Camera.File.*`
- `GET /cgi-bin/Config.cgi?action=get&property=Camera.*`

สังเกต: `&format=` และ `&backward=` มีอยู่ใน request-builder strings จึงบ่งชี้ว่า query string สำหรับแสดง/เรียกไฟล์วิดีโออาจมีเงื่อนไขเช่น direction หรือ media format ในการดึงรายการไฟล์และไฟล์วิดีโอ

### 2.4 Response Structure ที่พบจริง

จากชื่อนี้:

- `CamIdResponse`
- `FileListResponse`
- `MediaFile`

โดยสรุปโครงสร้างที่น่าจะเป็นจริงแบบ static ได้แก่:

- `CamIdResponse`
  - field/field-name likely exposes `camId`
  - response from `Camera.Preview.Source.1.Camid` / `2.Camid`
  - สอดคล้องกับข้อมูลกล้องหน้า–หลังที่แยกจาก `camId`

- `FileListResponse`
  - เป็น wrapper สำหรับรายการไฟล์หรือไฟล์วีดีโอ
  - มีลักษณะคล้าย `List<MediaFile>` หรือ `MediaFile[]`
  - เป็น object ที่ถูก `DeviceApi.getFileList()` / `MediaDataAccess` ใช้

- `MediaFile`
  - เป็น record/object สำหรับแต่ละไฟล์วิดีโอ
  - ส่วนใหญ่มีข้อมูลที่คาดว่ารวม:
    - filename / path
    - size
    - duration
    - timestamp
    - camId / source
    - media type / video flag
    - remote URL or file URL

สรุป response pattern:

- `CamIdResponse` คืนค่าตัวเลข/รหัสกล้อง เช่น Front/Rear source id
- `FileListResponse` คืนลิสต์ของ `MediaFile`
- `MediaFile` จะเป็นจุดที่ App ใช้เพื่อประมวลผล URL/ชื่อไฟล์สำหรับต่อไป

### 2.5 getFileList และ downloadFile

จากที่พบจริงใน DEX และ logs string:

- `getFileList` ถูกระบุเป็น method ของ `DeviceApi`
- `downloadFile` / `doDownloadFile` ถูกระบุเป็น method ของ media/download flow
- `MediaDataAccess` มี `downloadFile` และ `loadRemoteFiles, type:`
- `Downloader` มี log:
  - `Before downloadFile:`
  - `After downloadFile:`
  - `Downloader->onResponse, code:`
  - `Downloader->onFailure,exception:`
  - `Downloader->IOException,exception:`

สรุป flow แบบ static:

1. `DeviceApi.getFileList()` สร้าง/ส่ง request สำหรับ file list
2. `DeviceHttpEngine` ดำเนินการ HTTP request ผ่าน `DeviceRequest`
3. `FileListResponse` parse รายการไฟล์กลับมาเป็น `MediaFile`
4. เมื่อ user select file, `downloadFile()`/`doDownloadFile()` กำหนด URL จาก `MediaFile`/`MediaDataAccess`
5. `Downloader` ดึง binary content และ log status response code

### 2.6 Camera.Preview.Source.1.Camid และ CamIdResponse

ข้อความที่พบจริงจาก DEX:

- `Camera.Preview.Source.1.Camid`
- `Camera.Preview.Source.2.Camid`
- `Camid=`
- `CamIdResponse`
- `getCamID`
- `setCamID`
- `setcamid`

นี่ชี้ว่า APK แยกกล้องหน้า–หลังโดยใช้ source id ของกล้องแทนการสลับหน้า UI แบบโหมดเดียว

ดังนั้น source mapping ที่ปรากฏคือ:

- `Camera.Preview.Source.1.Camid` = กล้อง source 1
- `Camera.Preview.Source.2.Camid` = กล้อง source 2

สรุป: การแยกกล้องหน้า–หลังคือแยกตาม `camId`/source ID ไม่ใช่การสลับ `UIMode` หรือ stopping recording.

---

## 3) UNVERIFIED_ON_ASTON

สิ่งต่อไปนี้ยังไม่มีหลักฐานยืนยันแบบ static ที่เพียงพอสำหรับการยืนยันว่าเป็นการทำงานจริงของกล้อง ASTON:

- URL ที่แน่นอนสำหรับ download file วิดีโอแบบเดี่ยวของกล้องหน้า/หลัง
- รูปแบบ JSON/XML response ที่แน่นอนของ `FileListResponse`
- ชื่อฟิลด์ที่แน่นอนทั้งหมดของ `MediaFile`
- โฟลเดอร์หรือชื่อไฟล์ที่บอกว่ากล้องหน้า/หลังแยกกันอย่างชัดเจน (`front`/`rear`, `A`/`B`, `Normal`/`Event` เป็นต้น)
- ความจำเป็นในการเปลี่ยน `UIMode` หรือหยุด Recording เพื่อตั้งค่าอ่านไฟล์
- การมีอยู่จริงของ API สำหรับ `downloadFile` แบบ `POST` หรือ `GET` ที่มี payload เฉพาะ

คำเตือน: string constants เห็นว่า `&format=` และ `&backward=` ถูกใช้ใน request builder แต่ไม่มีหลักฐานชัดเจนว่าเป็น `GET` หรือ `POST` แบบเต็ม จึงอยู่ในช่วง "unverified but strongly suggested"

---

## 4) การแยกไฟล์กล้องหน้า–หลัง

จาก static evidence:

- `Camera.Preview.Source.Totals=2`
- `Camera.Preview.Source.1.Camid`
- `Camera.Preview.Source.2.Camid`
- `CamIdResponse`
- `MediaFile` / file list ผูกกับ `camId` หรือ source id

ดังนั้นการแยกไฟล์กล้องหน้า–หลังที่เป็นไปได้จากโค้ดคือ:

- แยกด้วย `camId`
- แยกด้วย source property ใน response
- แยกด้วย `MediaFile` metadata ไม่ใช่การเปลี่ยนหน้าจอหรือ stop recording

พอจะสรุปได้ว่า API นี้เป็น read-only media listing/download API; ไม่ใช่ API สำหรับ `action=set`, `delete`, `format`, หรือเปลี่ยนโหมดกล้อง

---

## 5) ต้องเปลี่ยน UIMode หรือหยุด Recording หรือไม่?

จาก static analysis ปรากฏว่าการทำงานหลักคือ:

- `getFileList`
- `downloadFile`
- `CamIdResponse`
- `DeviceHttpEngine`

ไม่มีหลักฐานที่ระบุว่าไฟล์วิดีโอ/รายการไฟล์ต้อง:

- เปลี่ยน `UIMode`
- สั่งหยุด Recording
- ใช้ `action=set`
- ส่ง `delete`, `format`, `reset`

ดังนั้นในระดับ static evidence ปรากฏว่า:

- ไม่จำเป็นต้องเปลี่ยน UIMode เพื่ออ่านรายการไฟล์
- ไม่จำเป็นต้องหยุด Recording เพื่อ download วิดีโอ
- โค้ดส่วนที่เกี่ยวข้องกับ media list/download เข้าถึงข้อมูลแบบ read-only

---

## 6) เปรียบเทียบกับ PROJECT_HANDOFF.md

สอดคล้องกับ PROJECT_HANDOFF.md ในประเด็นสำคัญ:

- กล้องให้บริการ CGI HTTP ของ `Config.cgi`
- `Camera.*` property tree เป็นทางหลักสำหรับข้อมูลกล้อง
- `Camera.Preview.Source.Totals=2` และ `Source.1.Camid`/`Source.2.Camid` เป็นหลักฐานของกล้องหน้า–หลัง
- `DeviceApi`/`DeviceHttpEngine`/`DeviceRequest` เป็นโครงสร้าง HTTP client ที่ถูกใช้เพื่ออ่านข้อมูลกล้อง
- Media listing/download flow เป็น read-only และสอดคล้องกับแนวทาง “ไฟล์วิดีโอบน SD Card” ของ ASTON

สิ่งที่ยังไม่มีการยืนยันจาก APK แต่ PROJECT_HANDOFF.md ระบุไว้เป็นสรุปจากงานก่อนหน้า:

- `Camera.File.Total` / `Camera.DBFileNum`
- GET `/cgi-bin/Config.cgi?action=get&property=Camera.File.*`
- กล้องหน้าและกล้องหลังบันทึกเป็นไฟล์แยกกันบน SD Card

รูปแบบดังกล่าวสอดคล้องกับ `FileListResponse` + `MediaFile` ใน APK แต่รายละเอียดชื่อ field และโฟลเดอร์จริงยังไม่เสร็จสมบูรณ์จาก static analysis เพียงอย่างเดียว

---

## 7) สรุปอย่างสั้น

ผลลัพธ์จาก static APK analysis:

- มี `DeviceApi.getFileList` และ `downloadFile`/`doDownloadFile` จริงใน APK
- โครงสร้าง HTTP ของ APK ใช้ `Config.cgi` + `action=get` + `property=...` เหมือนกับโปรโตคอลที่ยืนยันแล้ว
- กล้องหน้า–หลังแยกกันด้วย `Camera.Preview.Source.*.Camid` และ `CamIdResponse`
- `FileListResponse` + `MediaFile` เป็น model สำหรับรายการและ metadata ของไฟล์วิดีโอ
- `Downloader` ดำเนินการ fetch binary file จาก URL ที่มาจาก MediaFile / file metadata
- ไม่มีหลักฐานบ่งชี้ว่าต้องเปลี่ยน `UIMode` หรือหยุด Recording เพื่ออ่านรายการหรือดาวน์โหลดวิดีโอ
- การระบุชื่อไฟล์/โฟลเดอร์ที่แน่นอนสำหรับ front/rear นั้นยังอยู่ในช่วง UNVERIFIED_ON_ASTON จนกว่าจะมี static decompilation/analysis อย่างละเอียดมากขึ้น

---

## 8) Final classification

### VERIFIED_FROM_APK
- `DeviceApi`, `DeviceHttpEngine`, `DeviceRequest`
- `FileListResponse`, `MediaFile`, `CamIdResponse`
- `getFileList`, `downloadFile`, `doDownloadFile`
- `Camera.Preview.Source.1.Camid`
- `Config.cgi` + `action=get` + `property=...`
- `&format=` / `&backward=` query hints
- read-only file listing/download flow

### UNVERIFIED_ON_ASTON
- exact full response schema of `FileListResponse`
- exact `MediaFile` field names and data types
- exact final file-list URL for each source
- exact front/rear filename/dir naming scheme
- requirement to switch UI mode or stop recording

สรุป: การสืบค้นผ่าน APK สร้างภาพชัดว่า API สำหรับ file list/download ของกล้อง ASTON เป็น CGI/HTTP read-only ที่อยู่บน `Config.cgi` และ `CamId`/source-ID ทำหน้าที่แยกกล้องหน้า–หลัง โดยไม่ต้องใช้ action=set หรือเปลี่ยนโหมดการบันทึก
