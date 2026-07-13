from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    class Category(models.TextChoices):
        DEVELOPMENT = "pembangunan", "Pembangunan"
        ECOTOURISM = "ekowisata", "Ekowisata"
        CULTURE = "budaya", "Budaya"
        PREPAREDNESS = "kesiapsiagaan", "Kesiapsiagaan"
        ANNOUNCEMENT = "pengumuman", "Pengumuman"

    title = models.CharField("Judul", max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField("Kategori", max_length=20, choices=Category.choices)
    summary = models.CharField("Ringkasan", max_length=300)
    body = models.TextField("Isi", blank=True)
    image_url = models.URLField("URL Gambar", blank=True)
    published_at = models.DateField("Tanggal Terbit", default=timezone.now)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Berita"
        verbose_name_plural = "Berita & Pengumuman"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:detail", args=[self.slug])
