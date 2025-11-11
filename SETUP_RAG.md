# 🤖 ขั้นตอนการเปิดใช้งาน RAG System

## สิ่งที่แก้ไขแล้ว ✅

1. **เพิ่ม `/process` endpoint** - สำหรับประมวลผลไฟล์ Excel และโหลดข้อมูลเข้า RAG
2. **เพิ่มฟังก์ชัน `filter_by_keywords`** - กรองกลุ่มสินค้าด้วยคำค้นหา
3. **แก้ไข imports** - ใช้ `langchain_community` แทน `langchain` เก่า
4. **อัปเดต requirements.txt** - ระบุ version ที่ถูกต้อง
5. **สร้างสคริปต์ติดตั้ง** - `install_rag.ps1` (Windows) และ `install_rag.sh` (Linux/Mac)

## วิธีการติดตั้ง 📦

### สำหรับ Windows (PowerShell):
```powershell
# 1. รันสคริปต์ติดตั้ง
.\install_rag.ps1

# หรือติดตั้งด้วยมือ:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### สำหรับ Linux/Mac:
```bash
# 1. ทำให้สคริปต์รันได้
chmod +x install_rag.sh

# 2. รันสคริปต์
./install_rag.sh

# หรือติดตั้งด้วยมือ:
source .venv/bin/activate  # หรือ venv/bin/activate
pip install -r requirements.txt
```

**⚠️ หมายเหตุ:** การติดตั้งจะใช้เวลา 5-10 นาที เพราะต้องดาวน์โหลด PyTorch, Transformers และ models

## การตั้งค่า API Key 🔑

### 1. รับ Claude API Key:
- ไปที่: https://console.anthropic.com/
- สร้าง API key ใหม่

### 2. ตั้งค่า Environment Variable:

**Windows PowerShell:**
```powershell
# ชั่วคราว (ใช้ได้จนกว่าจะปิด terminal)
$env:CLAUDE_API_KEY = "sk-ant-api03-xxxxx"

# ถาวร (ใช้ได้ตลอด)
[System.Environment]::SetEnvironmentVariable('CLAUDE_API_KEY', 'sk-ant-api03-xxxxx', 'User')
```

**Linux/Mac:**
```bash
# เพิ่มใน ~/.bashrc หรือ ~/.zshrc
export CLAUDE_API_KEY="sk-ant-api03-xxxxx"

# จากนั้น reload
source ~/.bashrc  # หรือ source ~/.zshrc
```

## การรันแอป 🚀

```powershell
# Windows
.\.venv\Scripts\Activate.ps1
python app.py

# Linux/Mac
source .venv/bin/activate
python app.py
```

## การใช้งาน RAG Features 🎯

### 1. อัปโหลดและประมวลผลไฟล์
- อัปโหลดไฟล์ Excel
- ตั้งค่า Similarity Threshold
- กดปุ่ม "▶️ Process Data"
- ระบบจะโหลดข้อมูลเข้า RAG อัตโนมัติ

### 2. ถาม-ตอบ (AI Search)
- กดปุ่ม "🤖 AI Search"
- พิมพ์คำถาม เช่น:
  * "กลุ่มไหนมียอดขายสูงสุด?"
  * "แนะนำสินค้าที่ควรมัดรวมกัน"
  * "วิเคราะห์แนวโน้มการขาย"

### 3. รับ Insights อัตโนมัติ
- กดปุ่ม "💡 Get Insights"
- ระบบจะวิเคราะห์และให้คำแนะนำ

### 4. กรองด้วย Keywords
- กดปุ่ม "🔍 Filter by Keywords"
- ใส่คำค้นหา (คั่นด้วย comma)
- เลือกการเรียงลำดับ

## การตรวจสอบว่าติดตั้งสำเร็จ ✓

รันคำสั่งนี้:
```powershell
python -c "from rag_langchain import AdvancedRAG; print('✅ RAG System Ready!')"
```

ถ้าไม่มี error แสดงว่าติดตั้งสำเร็จ!

## การแก้ปัญหา 🔧

### ปัญหา: Import Error
```
ImportError: cannot import name 'HuggingFaceEmbeddings'
```
**วิธีแก้:** ติดตั้ง langchain-community
```bash
pip install langchain-community
```

### ปัญหา: CUDA/GPU Error
**วิธีแก้:** ใช้ CPU version
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install faiss-cpu
```

### ปัญหา: API Key ไม่ทำงาน
**วิธีตรวจสอบ:**
```powershell
# Windows
echo $env:CLAUDE_API_KEY

# Linux/Mac
echo $CLAUDE_API_KEY
```

## ขนาดไฟล์และหน่วยความจำ 💾

- **Disk Space:** ~3-4 GB (PyTorch + models)
- **RAM Usage:** ~2-3 GB เมื่อรัน
- **First Run:** ช้า 1-2 นาที (ดาวน์โหลด embedding model)
- **Subsequent Runs:** เร็วขึ้น (~5-10 วินาที)

## ไฟล์ที่สร้างใหม่ 📄

- ✅ `install_rag.ps1` - สคริปต์ติดตั้งสำหรับ Windows
- ✅ `install_rag.sh` - สคริปต์ติดตั้งสำหรับ Linux/Mac
- ✅ `.env.example` - ตัวอย่างการตั้งค่า environment variables
- ✅ `RAG_GUIDE.md` - คู่มือการใช้งาน RAG
- ✅ `SETUP_RAG.md` - ไฟล์นี้

## ถัดไป 🎓

1. ติดตั้ง dependencies ด้วย `install_rag.ps1`
2. ตั้งค่า `CLAUDE_API_KEY`
3. รัน `python app.py`
4. ทดสอบอัปโหลดไฟล์
5. ลองใช้ AI Search!
