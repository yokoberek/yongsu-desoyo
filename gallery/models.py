from django.db import models


class Photo(models.Model):
    title = models.CharField("Judul", max_length=200)
    image_url = models.URLField("URL Gambar")
    order = models.PositiveSmallIntegerField("Urutan", default=0)
    is_published = models.BooleanField("Ditampilkan", default=True)

    class Meta:
        verbose_name = "Foto"
        verbose_name_plural = "Galeri Foto"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title
