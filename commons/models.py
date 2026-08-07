from django.db import models


class Statistic(models.Model):
    label = models.CharField("Label", max_length=120)
    value = models.PositiveIntegerField("Nilai")
    order = models.PositiveSmallIntegerField("Urutan", default=0)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Statistik"
        verbose_name_plural = "Statistik Kampung"
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class HeroSlide(models.Model):
    title = models.CharField("Judul", max_length=200)
    subtitle = models.CharField("Sub-judul", max_length=300, blank=True)
    caption = models.CharField("Kapsi", max_length=120, blank=True)
    image = models.ImageField("Gambar", upload_to="hero/")
    order = models.PositiveSmallIntegerField("Urutan", default=0)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slide"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class OfficialPosition(models.Model):
    class Group(models.TextChoices):
        GOVERNMENT = "pemerintah", "Pemerintah Kampung"
        DIVISION = "kaur", "Kepala Urusan"
        CUSTOM = "adat", "Lembaga Adat"

    group = models.CharField(
        "Kelompok", max_length=20, choices=Group.choices, default=Group.GOVERNMENT
    )
    position = models.CharField("Jabatan / Lembaga", max_length=150)
    name = models.CharField("Nama", max_length=150, blank=True)
    description = models.TextField("Keterangan", blank=True)
    photo = models.ImageField("Foto", upload_to="pejabat/", blank=True)
    order = models.PositiveSmallIntegerField("Urutan", default=0)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Struktur Pemerintahan"
        verbose_name_plural = "Struktur Pemerintahan"
        ordering = ["order", "id"]

    def __str__(self):
        return self.position
