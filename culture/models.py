from django.db import models


class Tradition(models.Model):
    class Icon(models.TextChoices):
        SHIELD = "shield", "Perisai"
        BAG = "bag", "Tas / Noken"
        BOOK = "book", "Buku / Bahasa"
        RITUAL = "ritual", "Ritual"

    name = models.CharField("Nama", max_length=150)
    summary = models.CharField("Ringkasan", max_length=300)
    icon = models.CharField("Ikon", max_length=10, choices=Icon.choices, default=Icon.RITUAL)
    order = models.PositiveSmallIntegerField("Urutan", default=0)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Budaya & Tradisi"
        verbose_name_plural = "Budaya & Tradisi"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
