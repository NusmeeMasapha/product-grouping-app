# วิธีการใช้งานระบบ RAG (AI Q&A)

## การตั้งค่า Claude API Key

### Windows PowerShell:
```powershell
# ตั้งค่าชั่วคราว (จนกว่าจะปิด terminal)
$env:CLAUDE_API_KEY = "your_api_key_here"

# ตั้งค่าถาวร
[System.Environment]::SetEnvironmentVariable('CLAUDE_API_KEY', 'your_api_key_here', 'User')
```

### Linux/Mac:
```bash
# เพิ่มใน ~/.bashrc หรือ ~/.zshrc
export CLAUDE_API_KEY="your_api_key_here"
```

## การติดตั้ง Dependencies

```bash
# ติดตั้ง Python packages
pip install -r requirements.txt
```

**หมายเหตุ**: การติดตั้ง PyTorch และ transformers อาจใช้เวลานาน

## ฟีเจอร์ RAG ที่ใช้งานได้

### 1. ถาม-ตอบ (Ask Questions)
- คลิกปุ่ม "🤖 AI Search" เพื่อเปิดช่องค้นหา
- พิมพ์คำถามเกี่ยวกับข้อมูลการขาย
- กด Enter หรือคลิก "Ask" เพื่อส่งคำถาม

**ตัวอย่างคำถาม:**
- "กลุ่มสินค้าไหนมียอดขายสูงสุด?"
- "แนะนำสินค้าที่ควรมัดรวมกัน (Bundle)"
- "เปรียบเทียบกลุ่มที่ 1 กับกลุ่มที่ 2"
- "สินค้าที่มียอดขายต่ำควรทำอย่างไร?"

### 2. รับ Insights อัตโนมัติ
- คลิกปุ่ม "💡 Get Insights"
- ระบบจะวิเคราะห์และแนะนำกลยุทธ์ทางธุรกิจ

### 3. กรองข้อมูลด้วย Keywords
- คลิกปุ่ม "🔍 Filter by Keywords"
- ใส่คำค้นหา (คั่นด้วยเครื่องหมายจุลภาค)
- เลือกการเรียงลำดับ (จำนวนสินค้า หรือ ยอดขาย)

## การแก้ปัญหา

### ถ้าไม่แสดงปุ่ม AI
- ตรวจสอบว่าตั้ง `CLAUDE_API_KEY` แล้วหรือยัง
- ดู console log ว่า RAG system initialized สำเร็จหรือไม่

### ถ้าตอบช้า
- ครั้งแรกจะช้าเพราะต้อง download embedding model
- ครั้งต่อไปจะเร็วขึ้น

### ถ้า Error
- ตรวจสอบว่า API key ถูกต้อง
- ตรวจสอบว่าติดตั้ง dependencies ครบ
- ดู terminal log เพื่อหา error message
