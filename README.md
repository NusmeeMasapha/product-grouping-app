# 🤖 Product Grouping with AI Assistant

แอปพลิเคชันสำหรับจัดกลุ่มสินค้าอัตโนมัติและวิเคราะห์ข้อมูลด้วย AI

## ✨ ฟีเจอร์หลัก

### 📊 การจัดกลุ่มสินค้าอัตโนมัติ
- อัปโหลดไฟล์ Excel ที่มีข้อมูลสินค้า
- ระบบจะวิเคราะห์และจัดกลุ่มสินค้าที่คล้ายกันโดยอัตโนมัติ
- ใช้ TF-IDF และ Cosine Similarity ในการหาความคล้ายคลึง
- แสดงผลแบบ real-time พร้อมสถิติ

### 🤖 AI Assistant (RAG System)
- **ถาม-ตอบอิสระ**: ถามคำถามอะไรก็ได้เกี่ยวกับข้อมูลของคุณ
- **AI Insights**: รับคำแนะนำทางธุรกิจโดยอัตโนมัติ
- **การวิเคราะห์เชิงลึก**: AI จะวิเคราะห์และตอบคำถามจากข้อมูลจริง
- **ไม่ต้องใช้ Keywords**: ถามแบบธรรมชาติเหมือนคุยกับคน

## 🚀 วิธีการติดตั้ง

### 1. Clone Repository
```bash
git clone https://github.com/your-username/product-grouping-app.git
cd product-grouping-app
```

### 2. สร้าง Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. ติดตั้ง Dependencies

**แบบพื้นฐาน (ไม่มี AI):**
```bash
pip install Flask pandas openpyxl scikit-learn numpy Werkzeug
```

**แบบเต็ม (มี AI Assistant):**
```powershell
# Windows
.\install_rag.ps1

# Linux/Mac
chmod +x install_rag.sh
./install_rag.sh
```

### 4. ตั้งค่า API Key (สำหรับ AI features)

**รับ Claude API Key:**
1. ไปที่ https://console.anthropic.com/
2. สร้าง API key ใหม่

**ตั้งค่า Environment Variable:**

**Windows PowerShell:**
```powershell
# ชั่วคราว
$env:CLAUDE_API_KEY = "sk-ant-api03-xxxxx"

# ถาวร
[System.Environment]::SetEnvironmentVariable('CLAUDE_API_KEY', 'sk-ant-api03-xxxxx', 'User')
```

**Linux/Mac:**
```bash
export CLAUDE_API_KEY="sk-ant-api03-xxxxx"
```

### 5. รันแอปพลิเคชัน
```bash
python app.py
```

เปิดเบราว์เซอร์ที่: http://localhost:5000

## 📖 วิธีการใช้งาน

### ขั้นตอนพื้นฐาน:

1. **อัปโหลดไฟล์ Excel**
   - คลิก "📂 Upload Excel File"
   - เลือกไฟล์ที่มีคอลัมน์: `description` และ `sales_value`

2. **ตั้งค่า Similarity Threshold**
   - ค่า 0.0 - 1.0 (แนะนำ 0.3 - 0.7)
   - ค่ามากขึ้น = กลุ่มแยกมากขึ้น

3. **เลือกการเรียงลำดับ**
   - 💰 Total Sales Value: เรียงตามยอดขาย
   - 🔢 Count: เรียงตามจำนวนสินค้า

4. **กด "▶️ Process Data"**
   - รอประมวลผล
   - ดูผลลัพธ์และสถิติ

### ใช้งาน AI Assistant:

หลังจากประมวลผลข้อมูลแล้ว จะเห็น "🤖 AI Assistant" panel

**1. รับ Insights อัตโนมัติ:**
- กดปุ่ม "💡 Get Insights"
- AI จะวิเคราะห์และแนะนำ:
  - กลุ่มสินค้าที่น่าสนใจ
  - โอกาสทางธุรกิจ
  - คำแนะนำในการปรับปรุง

**2. ถาม-ตอบอิสระ:**
- พิมพ์คำถามในช่อง "ถามคำถามอะไรก็ได้..."
- กด Enter หรือคลิก "ถาม"

**ตัวอย่างคำถาม:**
```
- "กลุ่มไหนมียอดขายสูงสุด?"
- "แนะนำสินค้าที่ควรมัดรวมกัน"
- "เปรียบเทียบกลุ่มที่ 1 กับกลุ่มที่ 2"
- "สินค้าที่ขายไม่ดีควรทำอย่างไร?"
- "วิเคราะห์แนวโน้มการขาย"
```

ดูตัวอย่างเพิ่มเติมใน `AI_QUESTIONS.md`

## 📁 โครงสร้างโปรเจค

```
product-grouping-app/
├── app.py                 # Flask application
├── process.py             # Data processing logic
├── rag_langchain.py       # RAG/AI system
├── requirements.txt       # Python dependencies
├── install_rag.ps1        # Installation script (Windows)
├── install_rag.sh         # Installation script (Linux/Mac)
├── static/
│   └── index.css         # Styling
├── templates/
│   └── index.html        # Main UI
└── uploads/              # Uploaded files
```

## 🔧 การแก้ปัญหา

### AI Panel ไม่แสดง
- ตรวจสอบว่าตั้ง `CLAUDE_API_KEY` แล้ว
- ดู terminal log ว่า "RAG system initialized" หรือไม่
- ตรวจสอบว่าติดตั้ง langchain packages แล้ว

### Import Error
```bash
pip install langchain langchain-core langchain-community langchain-anthropic
```

### การตอบช้า (ครั้งแรก)
- ปกติ! ครั้งแรกต้องดาวน์โหลด embedding model
- ใช้เวลา 1-2 นาที
- ครั้งต่อไปจะเร็วขึ้น

### Memory Error
- ลดขนาดไฟล์ Excel
- ใช้ threshold สูงขึ้นเพื่อลดจำนวนกลุ่ม

## 📊 รูปแบบไฟล์ Excel

ไฟล์ Excel ต้องมีคอลัมน์:
- `description`: รายละเอียดสินค้า (text)
- `sales_value`: ยอดขาย (number)

**ตัวอย่าง:**
```
description              | sales_value
------------------------|------------
เสื้อยืดสีขาว          | 1500.00
กางเกงยีนส์            | 2500.00
```

## 🌟 คุณสมบัติพิเศษ

- ✅ รองรับภาษาไทยและอังกฤษ
- ✅ Real-time processing
- ✅ Responsive design (มือถือ/แท็บเล็ต)
- ✅ AI-powered insights
- ✅ Natural language Q&A
- ✅ ไม่ต้องใช้ keywords

## 📦 Dependencies

**Core:**
- Flask 3.0+
- pandas 2.0+
- scikit-learn 1.3+
- numpy 1.23+

**AI (Optional):**
- langchain
- langchain-anthropic
- sentence-transformers
- faiss-cpu
- transformers
- torch

## 🔒 ความปลอดภัย

- API key ควรเก็บใน environment variables
- อย่า commit API key ใน code
- ใช้ `.env` file หรือ system environment variables

## 📝 License

MIT License

## 👥 Contributing

Pull requests are welcome!

## 📧 Contact

สำหรับคำถามหรือข้อเสนอแนะ กรุณาติดต่อผ่าน GitHub Issues

---

**หมายเหตุ:** ระบบ AI ต้องการ Claude API Key และใช้ทรัพยากรพอสมควร (~3-4 GB disk space, 2-3 GB RAM)
