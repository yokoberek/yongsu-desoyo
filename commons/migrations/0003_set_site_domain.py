from django.conf import settings
from django.db import migrations


def set_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={"domain": "yongsu-dosoyo.id", "name": "Kampung Yongsu Desoyo"},
    )


def revert_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.filter(id=settings.SITE_ID).update(domain="example.com", name="example.com")


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("commons", "0002_heroslide_officialposition"),
    ]

    operations = [
        migrations.RunPython(set_site_domain, revert_site_domain),
    ]
