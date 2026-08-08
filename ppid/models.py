from django.db import models


class PpidTask(models.Model):
    text = models.CharField("Teks", max_length=300)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Tugas & Fungsi"
        verbose_name_plural = "Tugas & Fungsi"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class LegalBasis(models.Model):
    text = models.CharField("Teks", max_length=300)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Dasar Hukum"
        verbose_name_plural = "Dasar Hukum"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class PpidRole(models.Model):
    role_label = models.CharField("Peran PPID", max_length=100, help_text='Contoh: "Atasan PPID", "Ketua PPID"')
    official = models.ForeignKey(
        "commons.OfficialPosition", verbose_name="Dijabat oleh", on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Dipilih dari Struktur Pemerintahan.",
    )
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Struktur Pengelola PPID"
        verbose_name_plural = "Struktur Pengelola PPID"
        ordering = ["order", "id"]

    def __str__(self):
        return self.role_label


class InfoClassification(models.Model):
    badge_letter = models.CharField("Huruf Lencana", max_length=2, help_text='Contoh: "B", "S", "T", "D"')
    title = models.CharField("Judul", max_length=150)
    description = models.CharField("Deskripsi", max_length=300)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Klasifikasi Informasi"
        verbose_name_plural = "Klasifikasi Informasi"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class InfoClassificationItem(models.Model):
    classification = models.ForeignKey(
        InfoClassification, on_delete=models.CASCADE, related_name="items", verbose_name="Klasifikasi"
    )
    text = models.CharField("Teks", max_length=200)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Poin Klasifikasi Informasi"
        verbose_name_plural = "Poin Klasifikasi Informasi"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class RequestStep(models.Model):
    title = models.CharField("Judul", max_length=100)
    description = models.CharField("Deskripsi", max_length=300)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Langkah Permohonan"
        verbose_name_plural = "Langkah Permohonan"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class RequestRequirement(models.Model):
    text = models.CharField("Teks", max_length=300)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Syarat Permohonan"
        verbose_name_plural = "Syarat Permohonan"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class FaqItem(models.Model):
    question = models.CharField("Pertanyaan", max_length=300)
    answer = models.TextField("Jawaban")
    order = models.PositiveSmallIntegerField("Urutan", default=0)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["order", "id"]

    def __str__(self):
        return self.question
