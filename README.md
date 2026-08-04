# Ayesha Khan Singapore Overseas
### Enterprise Visa, Passport & Document Management System

এই প্রজেক্টটি আপনার **Master Developer Bible V2** অনুযায়ী তৈরি একটি সম্পূর্ণ Django-ভিত্তিক
Enterprise ওয়েব অ্যাপ্লিকেশন। নিচে ধাপে ধাপে সেটআপ, ব্যবহার ও ভবিষ্যৎ ফিচার চালু করার নির্দেশনা দেওয়া হলো।

---

## ১. প্রজেক্ট স্ট্রাকচার (Bible অধ্যায় ৫ অনুযায়ী)

```
ayesha_khan_project/
├── config/            # settings.py, urls.py, wsgi.py, asgi.py
├── accounts/          # login, logout, role management, audit log
├── dashboard/         # dashboard home, stats, smart search
├── agents/            # Agent Management
├── delegates/         # Delegate Management
├── passports/         # Passport Management + Movement History + AI/OCR hook
├── visa/               # Visa Processing + Visa Check
├── airtickets/         # Air Ticket Checking
├── documents/          # Document upload/categorize
├── reports/            # PDF / Excel Reports
├── notifications/      # Notification system + WhatsApp hook
├── company_settings/   # Company info, logo, backup settings
├── templates/           # Shared base.html + partials
├── static/              # CSS/JS
├── media/                # Uploaded files (passport scan, photo, signature ইত্যাদি)
├── manage.py
└── requirements.txt
```

---

## ২. Local Setup (নিজের কম্পিউটারে চালানোর জন্য)

### ধাপ ১: Virtual Environment তৈরি করুন
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### ধাপ ২: Requirements ইনস্টল করুন
```bash
pip install -r requirements.txt
```
> **নোট:** `pytesseract` কাজ করতে হলে সিস্টেমে আলাদাভাবে Tesseract OCR ইনস্টল থাকতে হবে
> (Ubuntu: `sudo apt install tesseract-ocr`, Windows: [UB-Mannheim Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki))

### ধাপ ৩: Environment Variables সেট করুন
`.env.example` ফাইলটি কপি করে `.env` নামে সেভ করুন এবং নিজের মান বসান:
```bash
cp .env.example .env
```
Local development-এ দ্রুত টেস্ট করতে চাইলে `.env` ফাইলে `DB_NAME` খালি রাখুন —
তাহলে স্বয়ংক্রিয়ভাবে SQLite ব্যবহার হবে (PostgreSQL সেটআপ ছাড়াই)।

### ধাপ ৪: Database তৈরি করুন
```bash
python manage.py makemigrations
python manage.py migrate
```

### ধাপ ৫: Super Admin তৈরি করুন
```bash
python manage.py createsuperuser
```

### ধাপ ৬: সার্ভার চালু করুন
```bash
python manage.py runserver
```
এরপর ব্রাউজারে যান: `http://127.0.0.1:8000/`
Admin প্যানেল: `http://127.0.0.1:8000/admin/`

---

## ৩. প্রথমবার লগইন করার পর যা করবেন

1. Admin panel (`/admin/`) থেকে লগইন করুন আপনার superuser দিয়ে।
2. **Settings** মেনু থেকে কোম্পানির নাম, লোগো, ঠিকানা বসান (Bible অধ্যায় ৫.৩)।
3. **User Management** থেকে অফিসের বাকি স্টাফদের জন্য অ্যাকাউন্ট তৈরি করুন এবং তাদের সঠিক Role
   (Admin / Office Staff / Data Entry Operator / Visa Processing Officer / Delegate Manager) দিন।

---

## ৪. যে ফিচারগুলো এখনই সম্পূর্ণ কাজ করবে

- ✅ Login/Logout, Role-based Access Control, Activity/Audit Log
- ✅ Agent, Delegate, Passport, Visa, Air Ticket, Document — সব CRUD + সার্চ + ফিল্টার
- ✅ Passport Movement History
- ✅ Visa স্ট্যাটাস workflow + status change audit trail
- ✅ Dashboard stats, Quick Actions, Smart Search
- ✅ PDF ও Excel রিপোর্ট এক্সপোর্ট (Passport, Visa, Agent, Delegate)
- ✅ Notification system (in-app)

## ৫. যেসব ফিচারের জন্য আপনার নিজের সেটআপ/API Key লাগবে (Bible-এ "ভবিষ্যৎ ফিচার" হিসেবে উল্লেখ ছিল)

### 🔹 AI Passport OCR (passports/ocr.py)
- সার্ভারে Tesseract OCR ইনস্টল করুন
- `.env`-এ `OCR_ENABLED=True` ও সঠিক `TESSERACT_CMD` পাথ দিন
- আরও নির্ভুল ফলাফলের জন্য ভবিষ্যতে `passporteye` লাইব্রেরি অথবা Google Vision / AWS Textract
  API যোগ করার সুপারিশ করা হলো — শুধু `extract_passport_data()` ফাংশন পরিবর্তন করলেই হবে।

### 🔹 WhatsApp Notification (notifications/whatsapp.py)
- Meta WhatsApp Business Cloud API সেটআপ করুন: https://developers.facebook.com/
- Phone Number ID ও Access Token সংগ্রহ করে `.env`-এ বসান
- `WHATSAPP_ENABLED=True` করুন
- এরপর `send_whatsapp_message()` ফাংশন স্বয়ংক্রিয়ভাবে কাজ শুরু করবে

### 🔹 Email Notification
- `.env`-এ আপনার SMTP তথ্য (Gmail App Password ইত্যাদি) বসান

### 🔹 Expiry Reminder Cron Job (স্বয়ংক্রিয় নোটিফিকেশন তৈরি)
প্রতিদিন একবার এই কমান্ড চালালে পাসপোর্ট/ভিসা মেয়াদ শেষের রিমাইন্ডার স্বয়ংক্রিয়ভাবে তৈরি হবে:
```bash
python manage.py generate_reminders
```
সার্ভারে crontab-এ যোগ করুন (প্রতিদিন সকাল ৮টায়):
```
0 8 * * * /path/to/venv/bin/python /path/to/project/manage.py generate_reminders
```

---

## ৬. প্রোডাকশনে Deploy করার সাধারণ ধাপ (যেকোনো VPS/Render/Railway-এ)

1. PostgreSQL ডাটাবেস তৈরি করুন এবং `.env`-এ কানেকশন তথ্য বসান
2. `.env`-এ `DEBUG=False` করুন এবং `ALLOWED_HOSTS`-এ আপনার ডোমেইন যোগ করুন
3. Static files কালেক্ট করুন:
   ```bash
   python manage.py collectstatic --noinput
   ```
4. Gunicorn দিয়ে চালান:
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```
5. Nginx (বা Render/Railway-এর built-in proxy) দিয়ে সামনে রাখুন এবং SSL (HTTPS) সেটআপ করুন
6. নিয়মিত ডাটাবেস ব্যাকআপ শিডিউল করুন

**দ্রুততম বিকল্প:** Render.com অথবা Railway.app-এ এই প্রজেক্ট আপলোড করলে তারা স্বয়ংক্রিয়ভাবে
`requirements.txt` পড়ে ইনস্টল করবে এবং PostgreSQL অ্যাড-অন যোগ করার অপশন দেবে — এতে
আপনার নিজের সার্ভার ম্যানেজ করা লাগবে না।

---

## ৭. ভবিষ্যৎ সম্প্রসারণ পরিকল্পনা (Bible ৫.১১ অনুযায়ী, ইতিমধ্যে scaffold করা আছে)

| ফিচার | বর্তমান অবস্থা |
|---|---|
| AI Passport & Visa Detection | `passports/ocr.py` স্ক্যাফোল্ড আছে, নিজের OCR/API key লাগবে |
| WhatsApp Integration | `notifications/whatsapp.py` স্ক্যাফোল্ড আছে |
| Email Notification | settings.py-তে কনফিগার আছে, SMTP তথ্য দিলেই চালু হবে |
| REST API | ভবিষ্যতে Django REST Framework যোগ করা যাবে |
| Client Online Portal | আলাদা app হিসেবে ভবিষ্যতে যোগ করা যাবে |
| Cloud Backup | `company_settings` মডেলে ফিল্ড রাখা আছে, স্ক্রিপ্ট যোগ করা যাবে |
| Face Match | ভবিষ্যতে face_recognition লাইব্রেরি দিয়ে যোগ করা যাবে |

---

## ৮. নিরাপত্তা সংক্রান্ত গুরুত্বপূর্ণ পরামর্শ

- প্রোডাকশনে যাওয়ার আগে অবশ্যই `SECRET_KEY` পরিবর্তন করুন (`.env`-এ)
- `DEBUG=False` রাখুন প্রোডাকশনে
- নিয়মিত `pip list --outdated` চেক করে সিকিউরিটি প্যাচ আপডেট রাখুন
- ডাটাবেস ব্যাকআপ নিয়মিত নিন এবং সার্ভারের বাইরে সংরক্ষণ করুন
