from django.db import models
from django.urls import reverse


class Destination(models.Model):
    class Category(models.TextChoices):
        NATURE = "alam", "Wisata Alam"
        MARINE = "bahari", "Bahari"
        UNDERWATER = "bawah_laut", "Bawah Laut"
        ECOTOURISM = "ekowisata", "Ekowisata"
        ADVENTURE = "petualangan", "Petualangan"
        LODGING = "menginap", "Menginap"

    name = models.CharField("Nama", max_length=150)
    slug = models.SlugField(unique=True)
    category = models.CharField("Kategori", max_length=20, choices=Category.choices)
    summary = models.CharField("Ringkasan", max_length=255)
    description = models.TextField("Deskripsi", blank=True)
    image_url = models.URLField("URL Gambar", blank=True)
    is_published = models.BooleanField("Ditampilkan", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Objek Wisata"
        verbose_name_plural = "Objek Wisata"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tourism:detail", args=[self.slug])
