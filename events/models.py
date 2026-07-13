from django.db import models
from django.utils import timezone


class Event(models.Model):
    class Category(models.TextChoices):
        CULTURE = "budaya", "Budaya"
        MARINE = "bahari", "Bahari"
        TRAINING = "pelatihan", "Pelatihan"
        GOVERNANCE = "pemerintahan", "Pemerintahan"

    title = models.CharField("Judul", max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField("Kategori", max_length=20, choices=Category.choices)
    summary = models.CharField("Ringkasan", max_length=300, blank=True)
    location = models.CharField("Lokasi", max_length=150, blank=True)
    start_date = models.DateField("Tanggal")
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Acara"
        verbose_name_plural = "Acara & Kegiatan"
        ordering = ["start_date"]

    def __str__(self):
        return self.title
