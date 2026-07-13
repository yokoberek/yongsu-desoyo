from django.db import models
from django.urls import reverse


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = "direncanakan", "Direncanakan"
        ONGOING = "berjalan", "Sedang Berjalan"
        DONE = "selesai", "Selesai"

    title = models.CharField("Judul", max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    summary = models.CharField("Ringkasan", max_length=300)
    description = models.TextField("Deskripsi", blank=True)
    image_url = models.URLField("URL Gambar", blank=True)
    status = models.CharField("Status", max_length=20, choices=Status.choices, default=Status.ONGOING)
    progress = models.PositiveSmallIntegerField("Progres (%)", default=0)
    year = models.PositiveSmallIntegerField("Tahun", null=True, blank=True)
    location = models.CharField("Lokasi", max_length=150, blank=True)
    funding_source = models.CharField("Sumber Dana", max_length=150, blank=True)
    implementer = models.CharField("Pelaksana", max_length=150, blank=True)
    is_published = models.BooleanField("Ditampilkan", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proyek Pembangunan"
        verbose_name_plural = "Program & Proyek"
        ordering = ["-year", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("development:detail", args=[self.slug])
