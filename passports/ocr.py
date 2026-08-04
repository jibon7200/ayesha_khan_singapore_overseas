"""
AI Passport Scan & OCR Automation - Bible অধ্যায় ৩ ও ১০ (ভবিষ্যৎ ফিচার)
------------------------------------------------------------------------
এই মডিউলটি একটি scaffold/hook হিসেবে রাখা হয়েছে। এটি এখনই কাজ করার জন্য আপনার
নিজের সার্ভারে Tesseract OCR ইনস্টল করতে হবে (অথবা settings.py-তে OCR_ENABLED=False
করে ম্যানুয়াল এন্ট্রি ব্যবহার করতে পারবেন)।

ইনস্টল নির্দেশনা (Ubuntu/Debian):
    sudo apt-get install tesseract-ocr
    pip install pytesseract pdf2image Pillow

MRZ (Machine Readable Zone) parsing আরও নির্ভুল করতে চাইলে ভবিষ্যতে
`passporteye` লাইব্রেরি অথবা কোনো paid Cloud OCR API (Google Vision,
AWS Textract) ব্যবহার করার সুপারিশ করা হলো - সেক্ষেত্রে এই ফাইলের
`extract_passport_data()` ফাংশনটি শুধু পরিবর্তন করলেই হবে, বাকি সিস্টেমে
কোনো পরিবর্তন লাগবে না।
"""
from django.conf import settings


def extract_passport_data(image_path: str) -> dict:
    """
    পাসপোর্ট ছবি থেকে টেক্সট বের করে একটি dict রিটার্ন করে:
    { holder_name, passport_number, nationality, date_of_birth,
      issue_date, expiry_date, gender, mrz_raw_text }

    এখনই ব্যবহারযোগ্য করতে করণীয়:
    1) সার্ভারে tesseract-ocr ইনস্টল করুন
    2) settings.py-তে OCR_ENABLED = True ও সঠিক TESSERACT_CMD পাথ দিন
    3) নিচের try ব্লকের ভেতরে pytesseract ব্যবহার করে প্রকৃত OCR যুক্ত হবে
    """
    if not settings.OCR_ENABLED:
        return {"error": "OCR বর্তমানে বন্ধ আছে (settings.OCR_ENABLED=False)।"}

    try:
        import pytesseract
        from PIL import Image

        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        image = Image.open(image_path)
        raw_text = pytesseract.image_to_string(image)

        # NOTE: এটি একটি বেসিক প্লেসহোল্ডার parser।
        # প্রকৃত MRZ parsing এর জন্য regex বা passporteye ব্যবহার করুন।
        return {
            "mrz_raw_text": raw_text,
            "holder_name": "",
            "passport_number": "",
            "nationality": "",
            "date_of_birth": None,
            "issue_date": None,
            "expiry_date": None,
            "gender": "",
            "note": "OCR টেক্সট বের হয়েছে, কিন্তু ফিল্ড-বাই-ফিল্ড parsing এখনও কনফিগার করা "
                    "হয়নি — MRZ regex/parser যোগ করলে স্বয়ংক্রিয়ভাবে ফর্ম ফিলআপ হবে।",
        }
    except Exception as exc:
        return {"error": f"OCR প্রসেসিং ব্যর্থ হয়েছে: {exc}"}
