import datetime
import time
import urllib.request

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from commons.models import HeroSlide, OfficialPosition, Statistic
from culture.models import Tradition
from development.models import Project
from events.models import Event, EventActivity
from gallery.models import Photo
from news.models import Post
from products.models import Product
from tourism.models import Destination

UNSPLASH = "https://images.unsplash.com/{id}?q=80&w=1600&auto=format&fit=crop"


def img(photo_id):
    return UNSPLASH.format(id=photo_id)


def fetch_image(photo_id):
    """A stock photo id ("photo-...") downloads from Unsplash; "local:..." reads a real photo
    already committed under static/, so ImageField-backed models get a real uploaded file either way."""
    if photo_id.startswith("local:"):
        path = settings.BASE_DIR / "static" / photo_id.removeprefix("local:")
        return ContentFile(path.read_bytes(), name=path.name)
    request = urllib.request.Request(img(photo_id), headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return ContentFile(response.read(), name=f"{photo_id}.jpg")
        except urllib.error.URLError:
            if attempt == 2:
                raise
            time.sleep(1.5)


def to_html(text):
    """Rich fields store HTML (edited via Unfold WYSIWYG); wrap seed paragraphs."""
    return "".join(f"<p>{p.strip()}</p>" for p in text.split("\n\n") if p.strip())


STATISTICS = [
    ("Jiwa Penduduk", 680),
    ("Kepala Keluarga", 152),
    ("Hektar Wilayah Adat", 23208),
    ("Destinasi Wisata", 6),
    ("Homestay Warga", 8),
    ("Keret / Marga Adat", 5),
]

HERO_SLIDES = [
    ("Di kaki Cycloop, di tepi Pasifik.", "Kampung Yongsu Desoyo — rumah masyarakat adat Tepra di pesisir utara Tanah Papua.", "Panorama Laut Pasifik", "photo-1507525428034-b723cf961d3e"),
    ("Air yang turun dari hutan Cycloop.", "Air Terjun Nantuke mengalir jernih, hanya beberapa langkah dari pemukiman warga.", "Air Terjun Nantuke", "photo-1432405972618-c60b0225b8f9"),
    ("Tempat Cenderawasih masih menari.", "Hutan adat yang dijaga turun-temurun, tempat satwa endemik Papua hidup bebas.", "Hutan Adat Cycloop", "photo-1470071459604-3b5ec3a7fe05"),
]

# group, position, name, description, photo
POSITIONS = [
    ("pemerintah", "Kepala Kampung", "Melkisedek Tablaseray", "", "local:images/people/melkisedek-tablaseray.png"),
    ("pemerintah", "Sekretaris Kampung", "", "", "photo-1494790108377-be9c29b29330"),
    ("pemerintah", "Bendahara Kampung", "", "", "photo-1500648767791-00dcc994a43e"),
    ("kaur", "Kaur Pemerintahan", "", "", "photo-1519085360753-af0119f7cbe7"),
    ("kaur", "Kaur Pembangunan", "", "", "photo-1560250097-0b93528c311a"),
    ("kaur", "Kaur Umum & Kesra", "", "", "photo-1573497019940-1c28c88b4f3e"),
    ("adat", "Ondoafi Besar", "", "Pemangku adat tertinggi yang menjaga wilayah, tatanan sosial, dan nilai-nilai leluhur kampung.", "photo-1568602471122-7832951cc4c5"),
    ("adat", "Dewan Adat Yewena Yosu", "", "Wadah musyawarah adat yang mengawal keputusan bersama demi kepentingan masyarakat kampung.", "photo-1544005313-94ddf0286df2"),
]

# name, category, summary, description, photo
DESTINATIONS = [
    ("Air Terjun Nantuke", "alam", "Air jernih dari hutan Cycloop, hanya beberapa langkah dari pemukiman warga.", "Air Terjun Nantuke adalah salah satu ikon alam Yongsu Desoyo. Airnya turun jernih dari hutan Pegunungan Cycloop dan mudah dijangkau dengan berjalan kaki singkat dari pemukiman.\n\nSuasananya teduh dan sejuk, cocok untuk melepas penat sambil menikmati suara hutan. Warga siap menemani sebagai pemandu.", "photo-1432405972618-c60b0225b8f9"),
    ("Pantai Sapari", "bahari", "Pantai berpasir di lereng Cycloop, tempat gunung bertemu Samudra Pasifik.", "Pantai Sapari menghadirkan pemandangan langka: lereng Pegunungan Cycloop yang langsung menyentuh birunya Samudra Pasifik. Pasirnya lembut dan perairannya tenang.\n\nTempat ideal untuk bersantai, berenang, hingga menikmati matahari terbit di ufuk timur Papua.", "photo-1507525428034-b723cf961d3e"),
    ("Snorkeling & Diving", "bawah_laut", "Terumbu karang sehat yang dijelajahi bersama pemandu selam setempat.", "Perairan Yongsu Desoyo menyimpan terumbu karang yang masih sehat dan beragam biota laut. Aktivitas snorkeling dan diving dipandu warga yang mengenal betul karakter perairan setempat.", "photo-1544551763-46a013bb70d5"),
    ("Birdwatching Cenderawasih", "ekowisata", "Mengamati Cenderawasih dan burung endemik di hutan adat yang masih perawan.", "Hutan adat Cycloop adalah rumah bagi Cenderawasih dan aneka burung endemik Papua. Bersama pemandu, pengunjung dapat mengamati satwa di habitat aslinya pada pagi hari.", "photo-1444464666168-49d633b86797"),
    ("Trekking Hutan Adat", "petualangan", "Menyusuri jalur hutan bersama pemandu lokal yang mengenal setiap sudut Cycloop.", "Jalur trekking membawa pengunjung menembus rimbun hutan adat, melewati sungai kecil dan pepohonan tua. Pemandu lokal berbagi cerita tentang kearifan warga menjaga hutan.", "photo-1441974231531-c6227db76b6e"),
    ("Homestay Warga", "menginap", "Menginap di rumah warga, merasakan langsung keseharian masyarakat Tepra.", "Homestay warga memberi pengalaman menginap yang hangat dan autentik. Tamu dapat ikut memasak, melaut, atau berkebun bersama tuan rumah sambil belajar budaya Tepra.", "photo-1507525428034-b723cf961d3e"),
]

# name, category, producer, summary, price_note, description, photo
PRODUCTS = [
    ("Hasil Laut Segar", "bahari", "Kelompok Nelayan Sapari", "Ikan, lobster, dan hasil tangkapan nelayan langsung dari perairan Pasifik.", "Harga pasar harian", "Hasil tangkapan nelayan Yongsu Desoyo dijual segar langsung dari perahu. Tersedia ikan, lobster, dan biota laut lain sesuai musim.", "photo-1544551763-46a013bb70d5"),
    ("Buah & Hasil Kebun", "agro", "Kelompok Tani Nantuke", "Mangga, durian, rambutan, dan umbi-umbian dari kebun warga di kaki Cycloop.", "Musiman", "Kebun warga di kaki Cycloop menghasilkan buah dan umbi berkualitas. Panen mengikuti musim, dengan rasa manis khas tanah Papua.", "photo-1519996529931-28324d5a630e"),
    ("Noken & Anyaman", "kriya", "UMKM Noken Mama Tepra", "Tas noken dan anyaman serat alami dengan motif khas, ditenun tangan warga.", "Rp150.000 – Rp500.000", "Noken ditenun tangan dari serat alami dengan motif khas. Setiap karya unik dan menjadi cinderamata bernilai budaya tinggi.", "photo-1519659528534-7fd733a832a0"),
    ("Hasil Hutan Bukan Kayu", "hutan", "Kelompok Hutan Lestari", "Madu, rempah, dan olahan hutan yang dipanen tanpa merusak ekosistem.", "Sesuai ketersediaan", "Madu hutan, rempah, dan olahan lain dipanen secara lestari dari hutan adat, menjaga ekosistem tetap seimbang.", "photo-1470071459604-3b5ec3a7fe05"),
    ("Olahan Pangan Lokal", "kuliner", "UMKM Dapur Cycloop", "Sagu, keladi, dan sajian khas yang disantap bersama hasil laut segar.", "Sesuai pesanan", "Sagu, keladi, dan sajian khas kampung diolah dengan resep turun-temurun. Nikmat disantap bersama hasil laut segar.", "photo-1518495973542-4542c06a5843"),
    ("Paket Ekowisata & Homestay", "jasa", "Pokdarwis Yongsu Desoyo", "Layanan pemandu, homestay, dan pengalaman berwisata yang dikelola warga.", "Mulai Rp250.000 / orang", "Paket ekowisata mencakup pemandu lokal, homestay warga, dan aktivitas seperti trekking, snorkeling, atau birdwatching sesuai minat.", "photo-1502082553048-f009c37129b9"),
]

TRADITIONS = [
    ("Kepemimpinan Ondoafi", "shield", "Sistem kepemimpinan adat yang menjaga tatanan sosial dan wilayah adat kampung."),
    ("Noken", "bag", "Tas serat alami bermotif khas, warisan budaya yang masih ditenun warga."),
    ("Bahasa Daerah", "book", "Bahasa ibu yang terus dijaga, dapat ditelusuri melalui Kamus Bahasa Raveni Rara."),
    ("Upacara & Tarian", "ritual", "Ritual dan kesenian yang menandai peristiwa penting dalam kehidupan warga."),
]

# title, category, date, photo, summary, body
POSTS = [
    ("Ruas Jalan Yongsu Sapari–Yongsu Desoyo Perkuat Konektivitas Pesisir", "pembangunan", datetime.date(2026, 6, 12), "photo-1470071459604-3b5ec3a7fe05", "Pembangunan ruas jalan penghubung antarkampung meningkatkan akses transportasi warga sekaligus membuka jalur baru bagi kunjungan wisata ke Yongsu Desoyo.", "Pembangunan ruas jalan Yongsu Sapari–Yongsu Desoyo menjadi tonggak penting bagi konektivitas kampung pesisir. Warga kini lebih mudah menjangkau pusat layanan dan pasar.\n\nJalur baru ini juga membuka akses bagi wisatawan, sekaligus mendukung distribusi hasil laut dan kebun warga."),
    ("Honai Homestay Dorong Ekonomi Berbasis Hutan", "ekowisata", datetime.date(2026, 1, 7), "photo-1441974231531-c6227db76b6e", "Pemanfaatan hasil hutan bukan kayu dan ekowisata menjadi pilihan warga untuk hidup sejahtera tanpa merusak hutan.", "Program honai homestay mengajak warga menyediakan hunian wisata berbasis rumah adat. Pendapatan dari tamu menjadi alternatif ekonomi yang ramah lingkungan.\n\nModel ini menegaskan bahwa kesejahteraan dapat tumbuh tanpa mengorbankan hutan adat."),
    ("Menuju Kampung Tangguh Bencana Hadapi Cuaca Ekstrem", "kesiapsiagaan", datetime.date(2025, 11, 3), "photo-1502082553048-f009c37129b9", "Warga bersama pemerintah memperkuat kesiapsiagaan menghadapi banjir dan perubahan iklim di wilayah pesisir.", "Melalui pelatihan dan simulasi, warga membangun kesiapsiagaan menghadapi banjir dan cuaca ekstrem. Peta risiko dan jalur evakuasi mulai disusun bersama.\n\nKampung tangguh bencana menjadi ikhtiar bersama menjaga keselamatan seluruh warga."),
    ("Persiapan Festival Budaya Tepra Libatkan Seluruh Warga", "budaya", datetime.date(2025, 12, 20), "photo-1519659528534-7fd733a832a0", "Warga bergotong royong menyiapkan tarian, upacara adat, dan pameran noken untuk festival tahunan kampung.", "Festival Budaya Tepra menjadi ajang merawat warisan leluhur. Warga dari berbagai keret bergotong royong menyiapkan tarian, upacara, dan pameran kerajinan.\n\nFestival ini juga menjadi daya tarik wisata budaya bagi pengunjung dari luar kampung."),
]

# title, category, date, location, summary, description, schedule (opsional, "" = belum tersedia), photo
# title, category, date, location, summary, description, activities (list of str, [] = belum tersedia), photo
EVENTS = [
    (
        "Festival Budaya Tepra", "budaya", datetime.date(2026, 8, 17), "Halaman Kampung",
        "Tarian, upacara adat, dan pameran noken di halaman kampung.",
        "Festival Budaya Tepra adalah perayaan tahunan yang menghadirkan tarian adat, upacara, dan pameran kerajinan noken karya warga.\n\nSeluruh keret (marga adat) turut ambil bagian, menjadikan festival ini ajang merawat identitas budaya sekaligus menyambut wisatawan yang ingin mengenal masyarakat adat Tepra lebih dekat.",
        [
            "Menyaksikan pawai dan pameran noken karya warga",
            "Menikmati pertunjukan tari adat Tepra",
            "Berbincang langsung dengan tetua adat dari berbagai keret",
            "Mencicipi kuliner khas yang disajikan warga",
        ],
        "photo-1519659528534-7fd733a832a0",
    ),
    (
        "Lomba Perahu & Bersih Pantai Sapari", "bahari", datetime.date(2026, 9, 14), "Pantai Sapari",
        "Adu dayung warga sekaligus aksi bersama menjaga pesisir tetap lestari.",
        "Kegiatan ini memadukan olahraga tradisional dan kepedulian lingkungan. Warga berlomba mendayung perahu sekaligus bergotong royong membersihkan sampah di sepanjang Pantai Sapari.\n\nAcara ini juga menjadi ajang mempererat kebersamaan antarwarga sambil menjaga kelestarian laut yang menjadi sumber kehidupan kampung.",
        [
            "Ikut kerja bakti membersihkan Pantai Sapari",
            "Menyaksikan atau mengikuti lomba dayung perahu tradisional",
            "Menikmati suasana pantai bersama warga",
        ],
        "photo-1507525428034-b723cf961d3e",
    ),
    (
        "Pelatihan Pemandu Ekowisata & Homestay", "pelatihan", datetime.date(2026, 10, 5), "Balai Kampung",
        "Membekali warga menyambut tamu dengan layanan ramah dan profesional.",
        "Pelatihan ini membekali warga yang mengelola homestay dan menjadi pemandu wisata dengan keterampilan pelayanan, keselamatan, serta pengetahuan tentang potensi alam dan budaya kampung.\n\nDiharapkan pelatihan ini meningkatkan kualitas layanan ekowisata Yongsu Desoyo secara berkelanjutan.",
        [],
        "photo-1441974231531-c6227db76b6e",
    ),
    (
        "Musyawarah Kampung Perencanaan 2027", "pemerintahan", datetime.date(2026, 11, 9), "Balai Kampung",
        "Warga dan pemerintah kampung menyusun rencana pembangunan bersama.",
        "Musyawarah Kampung (Muskam) adalah forum resmi warga bersama Pemerintah Kampung untuk membahas dan menyepakati rencana pembangunan tahun berikutnya.\n\nSetiap warga berhak menyampaikan usulan sesuai kebutuhan wilayah masing-masing sebagai bagian dari prinsip pemerintahan yang partisipatif.",
        [],
        "photo-1470071459604-3b5ec3a7fe05",
    ),
]

PHOTOS = [
    ("Panorama Samudra Pasifik", "photo-1507525428034-b723cf961d3e"),
    ("Air Terjun Nantuke", "photo-1432405972618-c60b0225b8f9"),
    ("Hutan Cycloop berkabut", "photo-1470071459604-3b5ec3a7fe05"),
    ("Cahaya menembus hutan", "photo-1518495973542-4542c06a5843"),
    ("Budaya adat Tepra", "photo-1519659528534-7fd733a832a0"),
    ("Dunia bawah laut", "photo-1544551763-46a013bb70d5"),
    ("Kegiatan warga di hutan", "photo-1441974231531-c6227db76b6e"),
    ("Perbukitan pesisir", "photo-1559128010-7c1ad6e1b6a5"),
    ("Hasil kebun warga", "photo-1519996529931-28324d5a630e"),
]

# title, status, progress, year, summary, description, location, funding_source, implementer, photo
PROJECTS = [
    (
        "Ruas Jalan Yongsu Sapari – Yongsu Desoyo", "berjalan", 75, 2026,
        "Membuka konektivitas darat antarkampung pesisir untuk warga dan kunjungan wisata.",
        "Proyek jalan penghubung ini mempermudah mobilitas warga dan distribusi hasil kampung, sekaligus membuka jalur kunjungan wisata.",
        "Ruas Yongsu Sapari – Yongsu Desoyo", "APBD Kabupaten Jayapura 2026", "Dinas Pekerjaan Umum dan Penataan Ruang Kabupaten Jayapura",
        "photo-1470071459604-3b5ec3a7fe05",
    ),
    (
        "Honai & Homestay Ekowisata", "selesai", 100, 2026,
        "Penyediaan hunian wisata berbasis warga untuk mendorong ekonomi dari ekowisata.",
        "Pembangunan honai homestay tahap pertama telah rampung dan mulai menerima tamu, menjadi sumber ekonomi baru bagi warga.",
        "Kampung Yongsu Desoyo", "Dana Desa 2026", "Swakelola Pemerintah Kampung",
        "photo-1441974231531-c6227db76b6e",
    ),
    (
        "Kampung Tangguh Bencana", "berjalan", 60, 2026,
        "Penguatan kesiapsiagaan warga menghadapi banjir dan cuaca ekstrem di wilayah pesisir.",
        "Program mencakup pelatihan, penyusunan jalur evakuasi, dan penguatan kelembagaan siaga bencana di tingkat kampung.",
        "Kampung Yongsu Desoyo", "Dana Desa 2026", "Badan Penanggulangan Bencana Daerah Kabupaten Jayapura",
        "photo-1502082553048-f009c37129b9",
    ),
    (
        "Jaringan Internet & Telekomunikasi", "berjalan", 45, 2026,
        "Peningkatan akses internet untuk mendukung layanan kampung dan belajar siswa.",
        "Perluasan jaringan bertujuan menghubungkan warga dan siswa dengan layanan digital serta informasi.",
        "Kampung Yongsu Desoyo", "APBN — Kementerian Komunikasi dan Digital", "Dinas Komunikasi dan Informatika Kabupaten Jayapura",
        "photo-1507525428034-b723cf961d3e",
    ),
    (
        "Dermaga / Pelabuhan Rakyat", "direncanakan", 20, 2027,
        "Sarana tambat perahu untuk memperlancar transportasi laut dan aktivitas nelayan.",
        "Dermaga rakyat direncanakan untuk memperlancar transportasi laut, kegiatan nelayan, dan kunjungan wisata melalui jalur laut.",
        "Pesisir Yongsu Desoyo", "APBD Provinsi Papua 2027", "Dinas Perhubungan Provinsi Papua",
        "photo-1544551763-46a013bb70d5",
    ),
]


class Command(BaseCommand):
    help = "Seed the database with sample village content (idempotent)."

    def handle(self, *args, **options):
        for order, (label, value) in enumerate(STATISTICS):
            Statistic.objects.update_or_create(label=label, defaults={"value": value, "order": order})

        for order, (title, subtitle, caption, photo) in enumerate(HERO_SLIDES):
            slide, _ = HeroSlide.objects.update_or_create(
                title=title,
                defaults={"subtitle": subtitle, "caption": caption, "order": order},
            )
            if not slide.image:
                file = fetch_image(photo)
                slide.image.save(file.name, file, save=True)

        for order, (group, position, name, description, photo) in enumerate(POSITIONS):
            official, _ = OfficialPosition.objects.update_or_create(
                position=position,
                defaults={"group": group, "name": name, "description": description, "order": order},
            )
            if photo and not official.photo:
                file = fetch_image(photo)
                official.photo.save(file.name, file, save=True)

        for name, category, summary, description, photo in DESTINATIONS:
            destination, _ = Destination.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "category": category, "summary": summary, "description": to_html(description)},
            )
            if not destination.image:
                file = fetch_image(photo)
                destination.image.save(file.name, file, save=True)

        for name, category, producer, summary, price_note, description, photo in PRODUCTS:
            product, _ = Product.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "category": category, "producer": producer, "summary": summary, "price_note": price_note, "description": to_html(description)},
            )
            if not product.image:
                file = fetch_image(photo)
                product.image.save(file.name, file, save=True)

        for order, (name, icon, summary) in enumerate(TRADITIONS):
            Tradition.objects.update_or_create(
                name=name, defaults={"icon": icon, "summary": summary, "order": order}
            )

        for title, category, date, photo, summary, body in POSTS:
            post, _ = Post.objects.update_or_create(
                slug=slugify(title),
                defaults={"title": title, "category": category, "published_at": date, "summary": summary, "body": to_html(body)},
            )
            if not post.image:
                file = fetch_image(photo)
                post.image.save(file.name, file, save=True)

        for title, category, date, location, summary, description, activities, photo in EVENTS:
            event, _ = Event.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "title": title, "category": category, "start_date": date, "location": location,
                    "summary": summary, "description": to_html(description),
                },
            )
            if not event.image:
                file = fetch_image(photo)
                event.image.save(file.name, file, save=True)
            for order, activity_title in enumerate(activities):
                EventActivity.objects.update_or_create(
                    event=event, order=order, defaults={"title": activity_title},
                )

        for order, (title, photo) in enumerate(PHOTOS):
            photo_obj, _ = Photo.objects.update_or_create(
                title=title, defaults={"order": order}
            )
            if not photo_obj.image:
                file = fetch_image(photo)
                photo_obj.image.save(file.name, file, save=True)

        for title, status, progress, year, summary, description, location, funding_source, implementer, photo in PROJECTS:
            project, _ = Project.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "title": title, "status": status, "progress": progress, "year": year, "summary": summary,
                    "description": to_html(description), "location": location, "funding_source": funding_source,
                    "implementer": implementer,
                },
            )
            if not project.image:
                file = fetch_image(photo)
                project.image.save(file.name, file, save=True)

        self.stdout.write(self.style.SUCCESS("Seed selesai."))
