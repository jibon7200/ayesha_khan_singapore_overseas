from .models import CompanyInfo


def company_info(request):
    """সব টেমপ্লেটে কোম্পানির নাম/লোগো ব্যবহারের জন্য গ্লোবাল কনটেক্সট।"""
    try:
        return {"company": CompanyInfo.load()}
    except Exception:
        return {"company": None}
