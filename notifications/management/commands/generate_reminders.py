"""
প্রতিদিন cron job দিয়ে চালানোর জন্য কমান্ড:
    python manage.py generate_reminders

Crontab উদাহরণ (প্রতিদিন সকাল ৮টায়):
    0 8 * * * /path/to/venv/bin/python /path/to/project/manage.py generate_reminders
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from passports.models import Passport
from visa.models import VisaApplication
from documents.models import Document
from notifications.models import Notification
from company_settings.models import CompanyInfo


class Command(BaseCommand):
    help = "পাসপোর্ট/ভিসা মেয়াদ শেষ হওয়ার রিমাইন্ডার ও পেন্ডিং ডকুমেন্ট অ্যালার্ট তৈরি করে।"

    def handle(self, *args, **options):
        company = CompanyInfo.load()
        today = timezone.localdate()

        # ---------------- Passport Expiry Reminder ----------------
        passport_deadline = today + timedelta(days=company.passport_expiry_alert_days)
        expiring_passports = Passport.objects.filter(
            expiry_date__isnull=False, expiry_date__lte=passport_deadline, expiry_date__gte=today,
        )
        created = 0
        for p in expiring_passports:
            _, was_created = Notification.objects.get_or_create(
                notification_type=Notification.NotificationType.PASSPORT_EXPIRY,
                title=f"পাসপোর্ট মেয়াদ শেষ হবে: {p.holder_name} ({p.passport_number})",
                defaults={
                    "message": f"মেয়াদ শেষ হওয়ার তারিখ: {p.expiry_date}",
                    "related_url": f"/passports/{p.pk}/",
                },
            )
            created += int(was_created)

        # ---------------- Visa Expiry Reminder ----------------
        visa_deadline = today + timedelta(days=company.visa_expiry_alert_days)
        expiring_visas = VisaApplication.objects.filter(
            visa_expiry_date__isnull=False, visa_expiry_date__lte=visa_deadline, visa_expiry_date__gte=today,
        )
        for v in expiring_visas:
            _, was_created = Notification.objects.get_or_create(
                notification_type=Notification.NotificationType.VISA_READY,
                title=f"ভিসা মেয়াদ শেষ হবে: {v.passport.holder_name} ({v.destination_country})",
                defaults={
                    "message": f"মেয়াদ শেষ হওয়ার তারিখ: {v.visa_expiry_date}",
                    "related_url": f"/visa/{v.pk}/",
                },
            )
            created += int(was_created)

        # ---------------- Ready for Delivery Reminder ----------------
        ready_passports = Passport.objects.filter(status=Passport.Status.READY_FOR_DELIVERY)
        for p in ready_passports:
            _, was_created = Notification.objects.get_or_create(
                notification_type=Notification.NotificationType.PASSPORT_RETURN,
                title=f"ডেলিভারির জন্য প্রস্তুত: {p.holder_name} ({p.passport_number})",
                defaults={"related_url": f"/passports/{p.pk}/"},
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"{created}টি নতুন নোটিফিকেশন তৈরি হয়েছে।"))
