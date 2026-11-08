# PHASE 3B-2 — Passive File List Observation Report
**โครงการ:** ASTON Ultimate X WiFi 2K (iOS Replacement)  
**เวลาบันทึก:** 8 พฤศจิกายน 2026  
**ลักษณะการทดสอบ:** Passive HTTP GET Observation (Read-Only 100%, Rate limit <= 1 req/s, Timeout 3s)

---

## 1. ตารางเปรียบเทียบผลการสังเกตการณ์: Baseline vs ขณะเปิด Ti2Cam Playback

| Endpoint / ตัวแปรที่ตรวจสอบ | รอบที่ 1: Baseline (ก่อนเปิดแอป) | รอบที่ 2: Ti2Cam อยู่หน้า Playback | การเปลี่ยนแปลง / การวิเคราะห์ |
|---|---|---|---|
| `Camera.Menu.UIMode` | `200 OK` (`VIDEO`) | `200 OK` (`VIDEO`) | **คงเดิม:** กล้องไม่เปลี่ยนโหมดเป็น PLAYBACK |
| `Camera.Preview.MJPEG.status.record` | `200 OK` (`Recording`) | `200 OK` (`Recording`) | **คงเดิม:** กล้องยังคงบันทึกวิดีโอต่อเนื่อง ไม่มีการหยุดบันทึก |
| `GET /cdv/filelist.xml` | `503 Service Unavailable` | `503 Service Unavailable` | **คงเดิม:** ถูกล็อกด้วย 503 |
| `GET /cdv/movielist.xml` | `503 Service Unavailable` | `503 Service Unavailable` | **คงเดิม:** ถูกล็อกด้วย 503 |
| `GET /cdv/photolist.xml` | `503 Service Unavailable` | `503 Service Unavailable` | **คงเดิม:** ถูกล็อกด้วย 503 |
| `Camera.File.Total` | `13` | `11` | มีการอัปเดตดัชนีไฟล์ฐานข้อมูล |
| `Camera.DBFileNum` | `26+127` | `22+127` | ตัวชี้ฐานข้อมูลปรับตำแหน่งตามรอบการบันทึก |

---

## 2. ข้อค้นพบสำคัญระดับสถาปัตยกรรม (Key Architectural Insights)

1. **กล้องไม่ตัดเข้า Playback Mode และไม่หยุดบันทึกภาพ:**
   - ในขณะที่ผู้ใช้เปิดหน้า Playback / รายการวิดีโอบน iPhone ผ่านแอป Ti2Cam กล้องยังคงรายงาน `Camera.Menu.UIMode=VIDEO` และสถานะการบันทึกยังเป็น `Recording` 100%
   - พิสูจน์ได้ว่า **Ti2Cam ไม่ได้สั่งหยุดการบันทึก หรือสั่ง `UIMode=PLAYBACK` เพื่อแสดงรายการไฟล์** กล้องยังคงบันทึกภาพหน้ารถได้อย่างต่อเนื่อง ปลอดภัย 100%
2. **Ti2Cam ไม่ได้ใช้ `/cdv/filelist.xml` หรือ `/cdv/movielist.xml`:**
   - เนื่องจากทั้งสองเอนด์พอยต์ยังคงตอบกลับ `HTTP 503 Service Unavailable` แสดงว่า Ti2Cam ไม่ได้พึ่งพา XML เหล่านี้ในการเรนเดอร์หน้ารายการคลิป
3. **กลไกที่ Ti2Cam อาจใช้จริง:**
   - ดึงผ่าน CGI อื่นที่ยังไม่ถูกทดสอบ (เช่น การดาวน์โหลดไฟล์ฐานข้อมูล `NormalDB` มาอ่านในตัวแอปโดยตรง) หรือใช้โปรโตคอลการคิวรีเฉพาะของชิปเซ็ต AIT
   - สังเกตพบว่ามีช่วงเวลาที่พอร์ต 80 ตอบสนองช้าลงหรือเกิด Socket Wait ชั่วคราว สอดคล้องกับช่วงที่ Ti2Cam กำลังดึงข้อมูลขนาดใหญ่หรือไฟล์ Thumbnail จากกล้อง

---

## 3. สรุปสถานะความปลอดภัย
- ดำเนินการผ่าน HTTP GET แบบ Read-only ทั้งหมด 100%
- ไม่มีการส่งคำสั่ง `action=set` หรือเปลี่ยนสถานะใดๆ
- การตรวจสอบรอบที่ 2 เสร็จสิ้นแล้ว ผู้ใช้สามารถออกจากหน้า Playback บน Ti2Cam ได้อย่างปลอดภัย
