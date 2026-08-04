"""
WhatsApp Business Cloud API Integration - Bible অধ্যায় ৩ ও ১০ (ভবিষ্যৎ ফিচার)
--------------------------------------------------------------------------
এখনই কাজ করানোর জন্য করণীয়:
1) https://developers.facebook.com/ থেকে WhatsApp Business Cloud API সেটআপ করুন
2) Phone Number ID ও Permanent Access Token সংগ্রহ করুন
3) .env ফাইলে WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN বসান, WHATSAPP_ENABLED=True করুন
4) নিচের send_whatsapp_message() ফাংশন স্বয়ংক্রিয়ভাবে কাজ শুরু করবে।

এই ফাইলে API-key hardcode করবেন না - সবসময় .env থেকে নিন (settings.py দেখুন)।
"""
import requests
from django.conf import settings


def send_whatsapp_message(phone_number: str, message: str) -> dict:
    """
    phone_number: আন্তর্জাতিক ফরম্যাটে, যেমন '65XXXXXXXX' (কান্ট্রি কোডসহ, + ছাড়া)
    message: পাঠানোর টেক্সট (passport ready, visa approved, ticket issued ইত্যাদি টেমপ্লেট)
    """
    if not settings.WHATSAPP_ENABLED:
        return {"status": "skipped", "reason": "WHATSAPP_ENABLED=False (settings.py / .env দেখুন)"}

    if not settings.WHATSAPP_API_URL or not settings.WHATSAPP_ACCESS_TOKEN:
        return {"status": "error", "reason": "WhatsApp API URL অথবা Access Token কনফিগার করা হয়নি।"}

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message},
    }
    try:
        response = requests.post(settings.WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return {"status": "sent", "response": response.json()}
    except requests.RequestException as exc:
        return {"status": "error", "reason": str(exc)}


# ---------------- রেডিমেড মেসেজ টেমপ্লেট (Bible অধ্যায় ১০ অনুযায়ী) ----------------

def passport_ready_message(holder_name: str) -> str:
    return f"প্রিয় {holder_name}, আপনার পাসপোর্ট রেডি হয়েছে। অফিস থেকে সংগ্রহ করুন। - Ayesha Khan Singapore Overseas"


def visa_approved_message(holder_name: str, country: str) -> str:
    return f"প্রিয় {holder_name}, আপনার {country}-এর ভিসা অনুমোদিত হয়েছে। বিস্তারিত জানতে অফিসে যোগাযোগ করুন।"


def ticket_issued_message(passenger_name: str, flight_number: str, travel_date: str) -> str:
    return f"প্রিয় {passenger_name}, আপনার টিকিট ইস্যু হয়েছে। ফ্লাইট: {flight_number}, তারিখ: {travel_date}।"
