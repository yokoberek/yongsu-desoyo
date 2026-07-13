from django.db import models
from django.urls import reverse


class Product(models.Model):
    class Category(models.TextChoices):
        MARINE = "bahari", "Bahari"
        AGRICULTURE = "agro", "Agro"
        CRAFT = "kriya", "Kriya"
        FOREST = "hutan", "Hutan"
        CULINARY = "kuliner", "Kuliner"
        SERVICE = "jasa", "Jasa"

    name = models.CharField("Nama", max_length=150)
    slug = models.SlugField(unique=True, max_length=150)
    category = models.CharField("Kategori", max_length=20, choices=Category.choices)
    producer = models.CharField("UMKM / Produsen", max_length=150, blank=True)
    summary = models.CharField("Ringkasan", max_length=255)
    description = models.TextField("Deskripsi", blank=True)
    specification = models.TextField("Spesifikasi", blank=True)
    price_note = models.CharField("Keterangan Harga", max_length=120, blank=True)
    image_url = models.URLField("URL Gambar", blank=True)
    is_published = models.BooleanField("Ditampilkan", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produk Lokal"
        verbose_name_plural = "Produk Lokal"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", args=[self.slug])
