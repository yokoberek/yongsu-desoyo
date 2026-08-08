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


class PageBanner(models.Model):
    key = models.SlugField(
        "Kunci Halaman", max_length=60, unique=True,
        help_text="Penanda teknis yang dipakai template untuk mencari banner ini -- jangan diubah.",
    )
    label = models.CharField("Nama Halaman", max_length=150)
    photo = models.ForeignKey(
        "gallery.Photo", verbose_name="Foto", on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Dipilih dari foto yang sudah diunggah di Galeri Foto.",
    )

    class Meta:
        verbose_name = "Banner Halaman"
        verbose_name_plural = "Banner Halaman"
        ordering = ["label"]

    def __str__(self):
        return self.label


# Bagian yang templatenya memang merender foto, lencana, atau kutipan. Hanya key ini
# yang menampilkan panel pelengkap di admin, supaya bagian lain tetap ringkas.
SECTIONS_WITH_FEATURE = frozenset({"home-about", "about-history"})


class PageSection(models.Model):
    """Teks pembuka sebuah bagian halaman -- label kecil, judul, dan isi. Daftar bagiannya
    ditentukan template lewat `key`, jadi admin hanya mengubah isinya, tidak menambah atau
    menghapus baris."""

    class Page(models.TextChoices):
        HOME = "beranda", "Beranda"
        ABOUT = "tentang", "Tentang Kampung"
        CONTACT = "kontak", "Kontak"
        PPID = "ppid", "PPID"

    key = models.SlugField(
        "Kunci Bagian", max_length=60, unique=True,
        help_text="Penanda teknis yang dipakai template untuk mencari bagian ini -- jangan diubah.",
    )
    page = models.CharField("Halaman", max_length=20, choices=Page.choices)
    label = models.CharField("Nama Bagian", max_length=150, help_text="Untuk memudahkan admin, tidak tampil di situs.")
    eyebrow = models.CharField(
        "Label Kecil", max_length=100, blank=True,
        help_text='Teks kecil di atas judul, mis. "Sekilas Kampung".',
    )
    heading = models.CharField("Judul", max_length=200, blank=True)
    body = models.TextField("Isi Teks", blank=True)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Teks Bagian Halaman"
        verbose_name_plural = "Teks Bagian Halaman"
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class SectionFeature(models.Model):
    """Pelengkap visual untuk bagian yang desainnya memang bergambar (lihat
    SECTIONS_WITH_FEATURE). Dipisah dari PageSection supaya form bagian biasa tidak
    dipenuhi isian yang templatenya tidak pernah render."""

    section = models.OneToOneField(
        PageSection, verbose_name="Bagian", on_delete=models.CASCADE, related_name="feature"
    )
    photo = models.ForeignKey(
        "gallery.Photo", verbose_name="Foto Utama", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="+", help_text="Dipilih dari foto yang sudah diunggah di Galeri Foto.",
    )
    photo_secondary = models.ForeignKey(
        "gallery.Photo", verbose_name="Foto Kedua", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="+", help_text="Foto kecil yang menimpa sudut foto utama -- hanya dipakai di beranda.",
    )
    badge_label = models.CharField("Label Lencana", max_length=60, blank=True, help_text='Contoh: "Terletak di"')
    badge_value = models.CharField("Isi Lencana", max_length=100, blank=True, help_text='Contoh: "Kaki Cycloop · Tepi Pasifik"')
    quote = models.CharField("Kutipan", max_length=300, blank=True, help_text="Hanya dipakai di bagian Sejarah Singkat.")

    class Meta:
        verbose_name = "Foto, Lencana & Kutipan"
        verbose_name_plural = "Foto, Lencana & Kutipan"

    def __str__(self):
        return f"Pelengkap {self.section.label}"


class SiteSettings(models.Model):
    """Singleton -- selalu satu baris (pk=1). Dipakai lewat context processor
    sehingga tersedia di semua template tanpa perlu diteruskan per-view."""

    email = models.EmailField("Email Kontak", default="info@yongsu-desoyo.id")
    phone_display = models.CharField("Telepon (tampilan)", max_length=30, default="0858-2446-6260")
    phone_e164 = models.CharField(
        "Telepon (format internasional)", max_length=20, default="+6285824466260",
        help_text="Format internasional dengan tanda +, contoh: +6285824466260",
    )

    class Meta:
        verbose_name = "Pengaturan Situs"
        verbose_name_plural = "Pengaturan Situs"

    def __str__(self):
        return "Pengaturan Situs"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactChannel(models.Model):
    key = models.SlugField(
        "Kunci", max_length=30, unique=True,
        help_text="Penanda teknis (menentukan ikon yang tampil) -- jangan diubah.",
    )
    label = models.CharField("Label", max_length=60)
    line1 = models.CharField("Baris 1", max_length=200, blank=True)
    line2 = models.CharField("Baris 2", max_length=200, blank=True)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Kanal Kontak"
        verbose_name_plural = "Kanal Kontak"
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class SocialLink(models.Model):
    key = models.SlugField(
        "Kunci", max_length=30, unique=True,
        help_text="Penanda teknis (menentukan ikon yang tampil) -- jangan diubah.",
    )
    label = models.CharField("Label", max_length=60)
    url = models.URLField("URL", blank=True)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Tautan Sosial Media"
        verbose_name_plural = "Tautan Sosial Media"
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class FastFact(models.Model):
    class Group(models.TextChoices):
        QUICK_FACTS = "quick_facts", "Fakta Ringkas (Tentang)"
        BOUNDARIES = "boundaries", "Batas Wilayah (Tentang)"

    group = models.CharField("Kelompok", max_length=20, choices=Group.choices)
    label = models.CharField("Label", max_length=100)
    value = models.CharField("Nilai", max_length=150)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Fakta Singkat"
        verbose_name_plural = "Fakta Singkat"
        ordering = ["group", "order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class MissionPoint(models.Model):
    text = models.CharField("Teks", max_length=300)
    order = models.PositiveSmallIntegerField("Urutan", default=0)

    class Meta:
        verbose_name = "Poin Misi"
        verbose_name_plural = "Poin Misi"
        ordering = ["order", "id"]

    def __str__(self):
        return self.text
