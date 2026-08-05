from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'ayeshakhansingaporeoverseas@gmail.com', 'adminpassword')

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
