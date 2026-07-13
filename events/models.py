from django.db import models
from django.urls import reverse


class Event(models.Model):
    class Category(models.TextChoices):
        CULTURE = "budaya", "Budaya"
        MARINE = "bahari", "Bahari"
        TRAINING = "pelatihan", "Pelatihan"
        GOVERNANCE = "pemerintahan", "Pemerintahan"

    title = models.CharField("Judul", max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    category = models.CharField("Kategori", max_length=20, choices=Category.choices)
    summary = models.CharField("Ringkasan", max_length=300, blank=True)
    description = models.TextField("Deskripsi", blank=True)
    location = models.CharField("Lokasi", max_length=150, blank=True)
    start_date = models.DateField("Tanggal")
    image_url = models.URLField("URL Gambar", blank=True)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Acara"
        verbose_name_plural = "Acara & Kegiatan"
        ordering = ["start_date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:detail", args=[self.slug])


class EventActivity(models.Model):
    """Hal yang bisa dilakukan/disaksikan pengunjung di acara ini (opsional, tanpa waktu tetap)."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="activities", verbose_name="Acara")
    title = models.CharField("Kegiatan", max_length=200)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Hal yang Bisa Dilakukan"
        verbose_name_plural = "Hal yang Bisa Dilakukan"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
