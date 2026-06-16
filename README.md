# EMD Exhibition — Registration & Dashboard System

ระบบลงทะเบียนงาน Event และ Dashboard สำหรับผู้จัดงาน  
สร้างด้วย HTML + React (CDN) + Firebase Firestore + GitHub Pages

🔗 **Live URL:** `https://souldabk7-ibizz.github.io/emd-registration/`

---

## ไฟล์หลัก

| ไฟล์ | หน้าที่ |
|------|---------|
| `Registration Form.html` | หน้าลงทะเบียนสำหรับลูกค้า (scan QR code) |
| `Event Dashboard.html` | หน้า Admin — ดูข้อมูล, export Excel, ล็อค event |
| `firebase-config.js` | ค่า config เชื่อมต่อ Firebase |

---

## Links ที่ใช้งาน

| ใช้งาน | URL |
|--------|-----|
| **ลูกค้า scan QR** | `.../Registration Form.html` |
| **Admin เท่านั้น** | `.../Event Dashboard.html` |

> ⚠️ URL ของ Dashboard ไม่ควรแชร์ให้ลูกค้า — ไม่มี password ป้องกัน

---

## วิธีใช้งาน (สำหรับ Admin)

### เปิด/ปิด Event สำหรับรับ register

1. เข้า **Dashboard** → เลือก tab event ที่ต้องการ
2. กดปุ่ม **"Open registration for Event X"** ในแถบสีเทาใต้ tabs
3. ทุก platform เห็นการเปลี่ยนแปลงทันที (realtime via Firestore)

> ระบบรองรับแค่ **1 active event** ต่อครั้ง — เมื่อเปิด event ใหม่ event เก่าปิดอัตโนมัติ

### ดูข้อมูล Participants

- Tab **Overview** — สถิติรวม, กราฟ, QR code, chart "By Industry" + "Products of Interest"
- Tab **Participants** — รายชื่อทั้งหมด, ค้นหา, แก้ไข, ลบ
- Tab **Analytics** — กราฟ trend รายวัน, top products, country breakdown

### Export ข้อมูลเป็น Excel

กดปุ่ม **Export Excel** มุมขวาบน  
→ ได้ไฟล์ `.xlsx` มีข้อมูลครบ รวมทั้ง Registration Date และ Time แยกคอลัมน์

---

## สิ่งที่ลูกค้าเห็น (Registration Form)

1. **Badge** บน hero: `● Now open: Event 1` — บอกว่า event ไหนกำลังเปิดรับ
2. **Header มุมขวา**: ชื่อ event + "Open for registration"
3. กรอกข้อมูล 4 ขั้นตอน → กด Submit → ได้ Registration ID
4. หน้า success มีแค่ปุ่ม **"Register Another Person"** — ไม่มี link ไป Dashboard

---

## Events

ปัจจุบันมี 4 event slots (ตั้งค่าใน `EVENT_CONFIG` ในแต่ละไฟล์):

```
Event 1 = EMD Technology Showcase 2026 (15–16 June 2026, Centara Grand, Bangkok)
Event 2 = TBD
Event 3 = TBD
Event 4 = TBD
```

เมื่อต้องการเพิ่มชื่อ/วันที่ event 2-4 → แก้ `EVENT_CONFIG` ใน `Event Dashboard.html` และ `Registration Form.html`

---

## Tech Stack

| ส่วน | เทคโนโลยี |
|------|-----------|
| Frontend | HTML + React 18 (CDN/Babel) |
| Database | Firebase Firestore (Spark free plan) |
| Hosting | GitHub Pages |
| Excel Export | SheetJS (xlsx) |
| QR Code | qrcodejs |

### Firestore Collections

```
participants/          ← ข้อมูล participant ทุก event (filter ด้วย eventId)
participants/_eventControl  ← เก็บ activeEvent (event ที่เปิดรับ register อยู่)
```

---

## การแก้ไข Event Config

เปิดทั้ง 2 ไฟล์ แล้วหา `EVENT_CONFIG` แก้ข้อมูลที่ต้องการ:

```js
const EVENT_CONFIG = {
  'emd-2026': {
    label: 'Event 1',
    name:  'EMD Technology Showcase 2026',
    date:  '15–16 June 2026',
    venue: 'Centara Grand Hotel, Bangkok',
  },
  'event-2': { label:'Event 2', name:'...', date:'...', venue:'...' },
  // ...
};
```

หลังแก้ → `git add . && git commit -m "..." && git push` → GitHub Pages deploy อัตโนมัติ (~1 นาที)

---

## Firestore Security Rules

ปัจจุบัน rules เปิดแค่ collection `participants` (read/write)  
Collection อื่น (`config` ฯลฯ) ถูก block โดย default

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /participants/{doc} {
      allow read, write: if true;
    }
  }
}
```

> หากต้องการ restrict ในอนาคต → เพิ่ม auth check ใน rules

---

*Powered by Ensys Motors and Drives Co., Ltd.*
