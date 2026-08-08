from django.db import migrations


def _html(*paragraphs):
    return "".join(f"<p>{p}</p>" for p in paragraphs)


# key, page, label, eyebrow, heading, body paragraphs -- urutannya mengikuti alur situs
# dan dipakai sebagai `order`, jadi daftar di admin terbaca seperti halamannya.
PAGE_SECTIONS = [
    (
        "home-about", "beranda", "Sekilas Kampung", "Sekilas Kampung",
        "Sebuah kampung di antara gunung dan samudra",
        [
            "Yongsu Desoyo adalah kampung masyarakat adat <strong>Suku Tepra</strong> di pesisir utara Tanah Papua. "
            "Punggung kampung bersandar pada rimbun <strong>Pegunungan Cycloop</strong>, sementara wajahnya menatap "
            "langsung hamparan <strong>Samudra Pasifik</strong>. Pertemuan gunung dan laut inilah yang membentuk "
            "denyut kehidupan warganya.",
            "Secara administratif, kampung ini berada di Distrik Ravenirara, Kabupaten Jayapura, Provinsi Papua. Tata "
            "ruang tradisionalnya ditata berdasarkan kearifan lokal yang diwariskan turun-temurun — dari zonasi kebun, "
            "tempat melaut, hingga ruang-ruang adat yang masih dijaga hingga kini.",
            "Di sini, hutan bukan sekadar latar belakang. Ia sumber pangan, obat, cerita, dan tempat Cenderawasih masih "
            "menari bebas. Warga menjaganya bukan karena aturan, melainkan karena hutan adalah bagian dari diri mereka.",
        ],
    ),
    (
        "home-highlights", "beranda", "Potensi Kampung", "Potensi Kampung",
        "Kekayaan yang tumbuh dari gunung, laut, dan adat",
        [
            "Sebagai desa wisata rintisan, Yongsu Desoyo menawarkan pengalaman yang jarang bisa dinikmati di satu "
            "tempat: air terjun, pantai, dunia bawah laut, satwa endemik, hingga tradisi yang masih hidup.",
        ],
    ),
    ("home-news", "beranda", "Buletin Kampung", "Buletin Kampung", "Kabar dari Yongsu Desoyo", []),
    ("home-stats", "beranda", "Kampung dalam Angka", "Kampung dalam Angka", "Denyut Yongsu Desoyo hari ini", []),
    ("home-events", "beranda", "Event Mendatang", "Event Mendatang", "Agenda kampung yang menanti Anda", []),
    (
        "home-cta", "beranda", "Rencanakan Kunjungan (CTA)", "Rencanakan Kunjungan",
        "Datang, singgah, dan tumbuh bersama kami di Yongsu Desoyo",
        [
            "Baik untuk berwisata, meneliti, maupun menjalin kerja sama pemberdayaan — kami menyambut Anda dengan "
            "tangan terbuka. Hubungi kami untuk mengatur kunjungan, homestay, dan paket ekowisata.",
        ],
    ),
    (
        "about-intro", "tentang", "Sekilas Kampung", "Sekilas Kampung",
        "Kampung yang tumbuh dari pertemuan gunung dan laut",
        [
            "Kampung Yongsu Desoyo terletak di Distrik Raveni Rara, Kabupaten Jayapura, Provinsi Papua. Kampung ini "
            "dihuni oleh masyarakat adat <strong>Suku Tepra</strong>, yang telah menetap dan menjaga wilayah ini "
            "secara turun-temurun.",
            "Letaknya istimewa: punggung kampung bersandar pada rimbun <strong>Pegunungan Cycloop</strong>, sementara "
            "wajahnya menatap langsung <strong>Samudra Pasifik</strong>. Sebagian besar warga bermata pencaharian "
            "sebagai nelayan dan petani, memadukan hasil laut dengan hasil kebun sebagai sumber kehidupan.",
            "Di tengah arus perubahan zaman, Yongsu Desoyo memilih jalan yang tidak menukar jati diri: melestarikan "
            "adat dan hutan warisan leluhur, sekaligus mengembangkan potensi ekonomi lokal melalui ekowisata, produk "
            "lokal, dan penguatan tata kelola kampung menuju status <strong>kampung adat</strong>.",
        ],
    ),
    (
        "about-geography", "tentang", "Geografi & Letak", "Geografi & Letak", "Di kaki Cycloop, di tepi Pasifik",
        [
            "Kampung ini berada di lereng utara Cagar Alam Pegunungan Cycloop yang langsung berbatasan dengan laut. "
            "Perpaduan ini menghadirkan kekayaan hayati yang jarang ditemui: hutan tropis dataran rendah, sungai dan "
            "air terjun, garis pantai, hingga ekosistem bawah laut.",
            "Akses menuju kampung dapat ditempuh melalui jalur darat maupun laut dari Kota Jayapura. Peningkatan "
            "konektivitas jalan antarkampung pesisir terus berlangsung untuk memudahkan warga dan kunjungan wisata.",
        ],
    ),
    (
        "about-history", "tentang", "Sejarah Singkat", "Sejarah Singkat",
        "Jejak Orang Tepra yang dijaga turun-temurun",
        [
            "Sejak lama, Orang Tepra menata ruang hidup mereka berdasarkan kearifan lokal — dari zonasi kebun, tempat "
            "melaut, hingga ruang-ruang adat. Tata ruang tradisional ini bukan sekadar pola permukiman, melainkan "
            "cerminan hubungan erat antara manusia, alam, dan leluhur.",
            "Kepemimpinan adat dipegang melalui sistem <strong>Ondoafi</strong>, yang menjadi penjaga tatanan sosial "
            "dan wilayah adat. Nilai-nilai inilah yang terus dirawat warga sembari kampung melangkah menuju pengakuan "
            "sebagai kampung adat.",
        ],
    ),
    (
        "about-culture-intro", "tentang", "Masyarakat & Budaya (pengantar)", "Masyarakat & Budaya",
        "Adat yang masih hidup di keseharian", [],
    ),
    (
        "about-vision", "tentang", "Visi", "Visi", "",
        [
            "Mewujudkan Yongsu Desoyo sebagai kampung adat yang mandiri, lestari, dan sejahtera — tempat kekayaan "
            "alam dan budaya menjadi sumber kehidupan yang berkelanjutan bagi seluruh warga.",
        ],
    ),
    (
        "about-structure-intro", "tentang", "Pemerintahan & Kelembagaan (pengantar)", "Pemerintahan & Kelembagaan",
        "Struktur yang menopang kampung",
        [
            "Pemerintahan kampung berjalan beriringan dengan lembaga adat. Keduanya bahu-membahu mengatur kehidupan "
            "warga, dari pelayanan sehari-hari hingga penjagaan wilayah adat.",
        ],
    ),
    (
        "about-cta", "tentang", "Ajakan Penutup (CTA)", "", "Ingin mengenal Yongsu Desoyo lebih jauh?",
        ["Jelajahi potensi wisata, produk lokal, dan program pembangunan kampung kami."],
    ),
    (
        "contact-message", "kontak", "Kirim Pesan", "Kirim Pesan",
        "Sampaikan pertanyaan atau rencana kunjungan Anda", [],
    ),
    (
        "contact-location", "kontak", "Lokasi", "Lokasi", "Temukan kami di peta",
        ["Kampung Yongsu Desoyo berada di pesisir utara, di kaki Pegunungan Cycloop, Distrik Raveni Rara."],
    ),
    (
        "ppid-home-intro", "ppid", "Tentang Layanan", "Tentang Layanan",
        "Informasi publik adalah hak setiap warga",
        [
            "Sesuai Undang-Undang No. 14 Tahun 2008 tentang Keterbukaan Informasi Publik, Pemerintah Kampung Yongsu "
            "Desoyo membentuk PPID untuk menyediakan, melayani, dan mendokumentasikan informasi publik secara "
            "terbuka, cepat, dan bertanggung jawab.",
            "Melalui layanan ini, masyarakat dapat mengakses informasi seputar penyelenggaraan pemerintahan kampung, "
            "perencanaan, anggaran, hingga hasil pembangunan.",
        ],
    ),
    ("ppid-request-steps", "ppid", "Alur Permohonan", "Alur Permohonan", "Empat langkah mudah", []),
    (
        "ppid-request-submit", "ppid", "Ajukan Melalui", "Ajukan Melalui", "",
        [
            "Permohonan dapat diajukan langsung ke Kantor Kampung pada jam pelayanan, atau melalui kontak resmi berikut.",
        ],
    ),
]

# key -> badge_label, badge_value, quote. Foto sengaja dibiarkan kosong; admin memilihnya
# dari Galeri Foto. Hanya key di SECTIONS_WITH_FEATURE yang boleh ada di sini.
SECTION_FEATURES = {
    "home-about": ("Terletak di", "Kaki Cycloop · Tepi Pasifik", ""),
    "about-history": (
        "Kearifan Lokal", "Tata Ruang Tradisional Tepra",
        "Menjaga adat dan hutan adalah cara kami menjaga diri sendiri.",
    ),
}

# key, label, line1, line2
CONTACT_CHANNELS = [
    ("address", "Alamat", "Kampung Yongsu Desoyo", "Distrik Raveni Rara, Kabupaten Jayapura, Provinsi Papua"),
    ("phone", "Telepon / WhatsApp", "0858-2446-6260", ""),
    ("email", "Email", "info@yongsu-desoyo.id", ""),
    ("hours", "Jam Pelayanan", "Senin – Jumat · 08.00 – 16.00 WIT", "Sabtu · 08.00 – 12.00 WIT"),
]

# key, label, url (kosong = belum ada, tampilkan sebagai placeholder)
SOCIAL_LINKS = [
    ("facebook", "Facebook", ""),
    ("instagram", "Instagram", ""),
    ("youtube", "YouTube", ""),
]

# group, label, value
FAST_FACTS = [
    ("quick_facts", "Provinsi", "Papua"),
    ("quick_facts", "Kabupaten", "Jayapura"),
    ("quick_facts", "Distrik", "Raveni Rara"),
    ("quick_facts", "Masyarakat Adat", "Suku Tepra"),
    ("quick_facts", "Bentang Alam", "Pesisir & Pegunungan"),
    ("quick_facts", "Status Wisata", "Desa Wisata Rintisan"),
    ("quick_facts", "Mata Pencaharian", "Nelayan & Petani"),
    ("boundaries", "Batas Utara", "Samudra Pasifik"),
    ("boundaries", "Batas Selatan", "Pegunungan Cycloop"),
]

MISSION_POINTS = [
    "Menjaga hutan, laut, dan wilayah adat sebagai warisan bersama.",
    "Mengembangkan ekowisata dan ekonomi warga yang berkeadilan.",
    "Melestarikan budaya, bahasa, dan pengetahuan tradisional Tepra.",
    "Memperkuat pemerintahan kampung yang transparan dan partisipatif.",
    "Meningkatkan layanan dasar: pendidikan, kesehatan, dan infrastruktur.",
]


def seed_content(apps, schema_editor):
    PageSection = apps.get_model("commons", "PageSection")
    SectionFeature = apps.get_model("commons", "SectionFeature")
    ContactChannel = apps.get_model("commons", "ContactChannel")
    SocialLink = apps.get_model("commons", "SocialLink")
    FastFact = apps.get_model("commons", "FastFact")
    MissionPoint = apps.get_model("commons", "MissionPoint")
    SiteSettings = apps.get_model("commons", "SiteSettings")

    SiteSettings.objects.get_or_create(pk=1)

    for order, (key, page, label, eyebrow, heading, paragraphs) in enumerate(PAGE_SECTIONS):
        section, _ = PageSection.objects.update_or_create(
            key=key,
            defaults={
                "page": page, "label": label, "eyebrow": eyebrow,
                "heading": heading, "body": _html(*paragraphs), "order": order,
            },
        )
        if key in SECTION_FEATURES:
            badge_label, badge_value, quote = SECTION_FEATURES[key]
            SectionFeature.objects.update_or_create(
                section=section,
                defaults={"badge_label": badge_label, "badge_value": badge_value, "quote": quote},
            )

    for order, (key, label, line1, line2) in enumerate(CONTACT_CHANNELS):
        ContactChannel.objects.update_or_create(
            key=key, defaults={"label": label, "line1": line1, "line2": line2, "order": order}
        )

    for order, (key, label, url) in enumerate(SOCIAL_LINKS):
        SocialLink.objects.update_or_create(key=key, defaults={"label": label, "url": url, "order": order})

    group_orders = {}
    for group, label, value in FAST_FACTS:
        order = group_orders.get(group, 0)
        group_orders[group] = order + 1
        FastFact.objects.update_or_create(group=group, label=label, defaults={"value": value, "order": order})

    for order, text in enumerate(MISSION_POINTS):
        MissionPoint.objects.update_or_create(text=text, defaults={"order": order})


def unseed_content(apps, schema_editor):
    PageSection = apps.get_model("commons", "PageSection")
    ContactChannel = apps.get_model("commons", "ContactChannel")
    SocialLink = apps.get_model("commons", "SocialLink")
    FastFact = apps.get_model("commons", "FastFact")
    MissionPoint = apps.get_model("commons", "MissionPoint")
    SiteSettings = apps.get_model("commons", "SiteSettings")

    # SectionFeature ikut terhapus lewat cascade dari PageSection.
    PageSection.objects.filter(key__in=[row[0] for row in PAGE_SECTIONS]).delete()
    ContactChannel.objects.filter(key__in=[row[0] for row in CONTACT_CHANNELS]).delete()
    SocialLink.objects.filter(key__in=[row[0] for row in SOCIAL_LINKS]).delete()
    FastFact.objects.all().delete()
    MissionPoint.objects.all().delete()
    SiteSettings.objects.filter(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0007_contactchannel_fastfact_missionpoint_pagesection_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_content, unseed_content),
    ]
