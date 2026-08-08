from django.db import migrations

PPID_TASKS = [
    "Menyediakan dan memberikan pelayanan informasi publik kepada masyarakat.",
    "Mengelola, mendokumentasikan, dan mengarsipkan informasi publik kampung.",
    "Menyusun daftar informasi publik yang wajib disediakan dan diumumkan.",
    "Melayani permohonan informasi dan menyelesaikan sengketa informasi secara adil.",
]

LEGAL_BASIS = [
    "UU No. 14 Tahun 2008 tentang Keterbukaan Informasi Publik",
    "UU No. 6 Tahun 2014 tentang Desa",
    "Peraturan Komisi Informasi tentang Standar Layanan Informasi Publik",
    "Peraturan Kampung tentang Pembentukan PPID",
]

# role_label -- "official" is left unset here; admin assigns who currently holds
# the role via the autocomplete field once Struktur Pemerintahan is filled in.
PPID_ROLES = ["Atasan PPID", "Ketua PPID", "Petugas Layanan"]

# badge_letter, title, description, [items]
INFO_CLASSIFICATIONS = [
    (
        "B", "Informasi Berkala", "Informasi yang wajib diumumkan secara rutin.",
        [
            "Profil dan struktur pemerintahan kampung",
            "Rencana Pembangunan (RPJM & RKP) Kampung",
            "Anggaran Pendapatan dan Belanja Kampung (APBKam)",
            "Laporan realisasi pelaksanaan kegiatan",
        ],
    ),
    (
        "S", "Informasi Serta-Merta",
        "Informasi yang wajib diumumkan tanpa penundaan karena menyangkut hajat hidup orang banyak.",
        [
            "Peringatan dini bencana (banjir, cuaca ekstrem)",
            "Informasi kesehatan dan wabah",
            "Gangguan layanan dasar kampung",
        ],
    ),
    (
        "T", "Tersedia Setiap Saat", "Informasi yang wajib disediakan dan dapat diakses melalui permohonan.",
        [
            "Peraturan dan keputusan kampung",
            "Data kependudukan dan wilayah",
            "Dokumen perencanaan dan hasil musyawarah",
            "Data aset dan inventaris kampung",
        ],
    ),
    (
        "D", "Informasi Dikecualikan",
        "Informasi tertentu dikecualikan dari akses publik sesuai peraturan, misalnya data pribadi warga dan "
        "informasi yang dapat mengganggu kepentingan yang dilindungi undang-undang.",
        [],
    ),
]

# title, description
REQUEST_STEPS = [
    ("Ajukan Permohonan", "Isi formulir permohonan dengan identitas dan rincian informasi yang diminta."),
    ("Registrasi", "Petugas PPID mencatat dan memberikan tanda bukti permohonan Anda."),
    ("Proses", "PPID memeriksa dan menyiapkan informasi paling lambat 10 hari kerja (dapat diperpanjang 7 hari)."),
    ("Pemberitahuan", "Informasi diberikan, atau pemohon menerima penjelasan bila permohonan ditolak."),
]

REQUEST_REQUIREMENTS = [
    "Fotokopi identitas diri (KTP) pemohon",
    "Rincian informasi yang dimohon sejelas mungkin",
    "Alasan/tujuan penggunaan informasi",
    "Untuk badan hukum: melampirkan akta dan surat kuasa",
]

# question, answer
FAQ_ITEMS = [
    (
        "Siapa yang boleh mengajukan permohonan informasi?",
        "Setiap warga negara Indonesia, baik perorangan maupun badan hukum, berhak mengajukan permohonan informasi "
        "publik dengan mengikuti prosedur yang berlaku.",
    ),
    (
        "Apakah dikenakan biaya?",
        "Pelayanan informasi pada dasarnya tidak dipungut biaya. Biaya hanya dapat dikenakan untuk penggandaan atau "
        "perekaman sesuai ketentuan, dan diberitahukan kepada pemohon terlebih dahulu.",
    ),
    (
        "Berapa lama informasi diberikan?",
        "PPID memberikan pemberitahuan paling lambat 10 hari kerja sejak permohonan diterima, dan dapat "
        "diperpanjang paling lama 7 hari kerja dengan pemberitahuan tertulis.",
    ),
    (
        "Bagaimana jika permohonan ditolak?",
        "Pemohon berhak mengajukan keberatan kepada atasan PPID. Bila belum puas, sengketa dapat dilanjutkan ke "
        "Komisi Informasi sesuai peraturan yang berlaku.",
    ),
]


def seed_content(apps, schema_editor):
    PpidTask = apps.get_model("ppid", "PpidTask")
    LegalBasis = apps.get_model("ppid", "LegalBasis")
    PpidRole = apps.get_model("ppid", "PpidRole")
    InfoClassification = apps.get_model("ppid", "InfoClassification")
    InfoClassificationItem = apps.get_model("ppid", "InfoClassificationItem")
    RequestStep = apps.get_model("ppid", "RequestStep")
    RequestRequirement = apps.get_model("ppid", "RequestRequirement")
    FaqItem = apps.get_model("ppid", "FaqItem")

    for order, text in enumerate(PPID_TASKS):
        PpidTask.objects.update_or_create(text=text, defaults={"order": order})

    for order, text in enumerate(LEGAL_BASIS):
        LegalBasis.objects.update_or_create(text=text, defaults={"order": order})

    for order, role_label in enumerate(PPID_ROLES):
        PpidRole.objects.update_or_create(role_label=role_label, defaults={"order": order})

    for order, (badge_letter, title, description, items) in enumerate(INFO_CLASSIFICATIONS):
        classification, _ = InfoClassification.objects.update_or_create(
            title=title, defaults={"badge_letter": badge_letter, "description": description, "order": order}
        )
        for item_order, text in enumerate(items):
            InfoClassificationItem.objects.update_or_create(
                classification=classification, text=text, defaults={"order": item_order}
            )

    for order, (title, description) in enumerate(REQUEST_STEPS):
        RequestStep.objects.update_or_create(title=title, defaults={"description": description, "order": order})

    for order, text in enumerate(REQUEST_REQUIREMENTS):
        RequestRequirement.objects.update_or_create(text=text, defaults={"order": order})

    for order, (question, answer) in enumerate(FAQ_ITEMS):
        FaqItem.objects.update_or_create(question=question, defaults={"answer": answer, "order": order})


def unseed_content(apps, schema_editor):
    PpidTask = apps.get_model("ppid", "PpidTask")
    LegalBasis = apps.get_model("ppid", "LegalBasis")
    PpidRole = apps.get_model("ppid", "PpidRole")
    InfoClassification = apps.get_model("ppid", "InfoClassification")
    RequestStep = apps.get_model("ppid", "RequestStep")
    RequestRequirement = apps.get_model("ppid", "RequestRequirement")
    FaqItem = apps.get_model("ppid", "FaqItem")

    PpidTask.objects.all().delete()
    LegalBasis.objects.all().delete()
    PpidRole.objects.filter(role_label__in=PPID_ROLES).delete()
    InfoClassification.objects.all().delete()
    RequestStep.objects.all().delete()
    RequestRequirement.objects.all().delete()
    FaqItem.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("ppid", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, unseed_content),
    ]
