# API Testing Lab — QuickPizza

งาน Lab นี้เป็นการทดสอบ QuickPizza API ในรายวิชา Software Quality Assurance and Testing โดยใช้ Python, requests และ pytest

## Requirements

- Python 3.10 or newer
- Git
- curl
- Visual Studio Code

## Installation

เปิด Terminal ในโฟลเดอร์โปรเจกต์ แล้วรันคำสั่ง:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the tests

รันทดสอบทั้งหมด:

```bash
pytest -v
```

สร้างรายงานผลการทดสอบแบบ HTML:

```bash
pytest -v --html=report.html --self-contained-html
```

เปิดไฟล์ `report.html` ในเบราว์เซอร์เพื่อดูผลของแต่ละ Test และรายละเอียดกรณีที่ไม่ผ่าน

หมายเหตุ: ชุดทดสอบเรียก API จริงที่ https://quickpizza.grafana.com จึงต้องเชื่อมต่ออินเทอร์เน็ต และการทดสอบทั้งหมดอาจใช้เวลาประมาณ 1 นาที ไม่ควรรันซ้ำต่อเนื่องหลายรอบ

## Input domain model — POST /api/ratings

การสร้าง Rating ใช้ลักษณะข้อมูล 4 ด้าน (Characteristics) โดยแบ่งเป็นกลุ่มข้อมูล (Blocks) ดังนี้

| Characteristic | Input blocks | Base choice / ตัวอย่าง | Test ที่ครอบคลุม |
|---|---|---|---|
| C1 — Value of stars | ต่ำกว่า 1, 1–5, มากกว่า 5 | 0, 3, 6 | `test_base_choice_is_saved`, `test_stars_out_of_range` |
| C2 — Type of stars | จำนวนเต็ม, ทศนิยม, ข้อความ, ไม่ส่งค่า | 3, 3.5, "3", ไม่ระบุ | `test_base_choice_is_saved`, `test_stars_decimal_is_refused`, `test_stars_text_is_refused`, `test_stars_missing_is_refused` |
| C3 — Pizza existence | มี Pizza อยู่จริง, ไม่มี Pizza | Pizza จาก Fixture, 999999999 | `test_base_choice_is_saved`, `test_nonexistent_pizza_is_refused` |
| C4 — Token | Token ถูกต้อง, ไม่ส่ง Token, Token ไม่ถูกต้อง | Token ของผู้ใช้ทดสอบ, ไม่มี Header, `token short` | `test_base_choice_is_saved`, `test_missing_token_is_refused`, `test_short_token_is_refused` |

**Base choice coverage:** ใช้ทั้งหมด **9 Tests** โดยเริ่มจากกรณีพื้นฐาน 1 กรณี แล้วเปลี่ยน Block ทีละส่วน ได้แก่ 1 + (3−1) + (4−1) + (2−1) + (3−1) = 9 Tests

**All combinations coverage:** หากทดสอบทุกชุดค่าผสม จะต้องใช้ 3 × 4 × 2 × 3 = **72 Tests**

## Safety and test independence

- Test ที่สร้าง Rating จะสร้างผู้ใช้ใหม่และใช้ Token ของผู้ใช้นั้นเอง
- Token ตัวอย่างใน `auth.txt` ใช้ตามขั้นตอน Lab เท่านั้น ห้ามใช้สร้าง แก้ไข หรือลบ Rating
- Test จะสร้างและจัดการข้อมูลที่จำเป็นสำหรับการทดสอบของตัวเอง
- `madeup.txt` เป็น Token สมมติ ใช้ทดสอบคำขอ GET ตามโจทย์เท่านั้น
- ไม่ใส่รหัสผ่านจริงหรือ API Key ส่วนตัวลงใน Repository

## Project files

- `conftest.py` — API session และ Fixtures สำหรับผู้ใช้ Pizza และ Rating
- `test_names.py`, `test_tools.py`, `test_pizza.py` — ทดสอบ API พื้นฐาน
- `test_users.py`, `test_refused.py` — ทดสอบการสร้างผู้ใช้และคำขอที่ถูกปฏิเสธ
- `test_ratings.py` — ทดสอบการจัดการ Rating
- `test_excluded_tools.py` — ทดสอบกรณี Excluded Tools และ Bug ที่พบ
- `test_create_rating.py` — ทดสอบการสร้าง Rating ตาม Input Domain Model
- `test_update_rating.py` — ทดสอบ Boundary Values ของ stars
- `test_rating_owner.py` — ทดสอบสิทธิ์การเข้าถึง Rating ของเจ้าของ
- `RESULTS.md` — ผลการทดลอง Defect report และคำตอบ Part B
- `report.html` — รายงานผลการทดสอบจาก pytest
