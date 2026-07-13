import datetime

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from commons.models import HeroSlide, OfficialPosition, Statistic
from culture.models import Tradition
from development.models import Project
from events.models import Event
from gallery.models import Photo
from news.models import Post
from products.models import Product
from tourism.models import Destination

UNSPLASH = "https://images.unsplash.com/{id}?q=80&w=1600&auto=format&fit=crop"


def img(photo_id):
    return UNSPLASH.format(id=photo_id)


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

# group, position, name, description
POSITIONS = [
    ("pemerintah", "Kepala Kampung", "", ""),
    ("pemerintah", "Sekretaris Kampung", "", ""),
    ("pemerintah", "Bendahara Kampung", "", ""),
    ("kaur", "Kaur Pemerintahan", "", ""),
    ("kaur", "Kaur Pembangunan", "", ""),
    ("kaur", "Kaur Umum & Kesra", "", ""),
    ("adat", "Ondoafi Besar", "", "Pemangku adat tertinggi yang menjaga wilayah, tatanan sosial, dan nilai-nilai leluhur kampung."),
    ("adat", "Dewan Adat Yewena Yosu", "", "Wadah musyawarah adat yang mengawal keputusan bersama demi kepentingan masyarakat kampung."),
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
    ("Buah & Hasil Kebun", "agro", "Kelompok Tani Nantuke", "Mangga, durian, rambutan, dan umbi-umbian dari kebun warga di kaki Cycloop.", "Musiman", "Kebun warga di kaki Cycloop menghasilkan buah dan umbi berkualitas. Panen mengikuti musim, dengan rasa manis khas tanah Papua.", "photo-1591207099859-cc47f28e1b3d"),
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

EVENTS = [
    ("Festival Budaya Tepra", "budaya", datetime.date(2026, 8, 17), "Halaman Kampung", "Tarian, upacara adat, dan pameran noken di halaman kampung."),
    ("Lomba Perahu & Bersih Pantai Sapari", "bahari", datetime.date(2026, 9, 14), "Pantai Sapari", "Adu dayung warga sekaligus aksi bersama menjaga pesisir tetap lestari."),
    ("Pelatihan Pemandu Ekowisata & Homestay", "pelatihan", datetime.date(2026, 10, 5), "Balai Kampung", "Membekali warga menyambut tamu dengan layanan ramah dan profesional."),
    ("Musyawarah Kampung Perencanaan 2027", "pemerintahan", datetime.date(2026, 11, 9), "Balai Kampung", "Warga dan pemerintah kampung menyusun rencana pembangunan bersama."),
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
    ("Hasil kebun warga", "photo-1591207099859-cc47f28e1b3d"),
]

# title, status, progress, year, summary, description
PROJECTS = [
    ("Ruas Jalan Yongsu Sapari – Yongsu Desoyo", "berjalan", 75, 2026, "Membuka konektivitas darat antarkampung pesisir untuk warga dan kunjungan wisata.", "Proyek jalan penghubung ini mempermudah mobilitas warga dan distribusi hasil kampung, sekaligus membuka jalur kunjungan wisata.", "photo-1470071459604-3b5ec3a7fe05"),
    ("Honai & Homestay Ekowisata", "selesai", 100, 2026, "Penyediaan hunian wisata berbasis warga untuk mendorong ekonomi dari ekowisata.", "Pembangunan honai homestay tahap pertama telah rampung dan mulai menerima tamu, menjadi sumber ekonomi baru bagi warga.", "photo-1441974231531-c6227db76b6e"),
    ("Kampung Tangguh Bencana", "berjalan", 60, 2026, "Penguatan kesiapsiagaan warga menghadapi banjir dan cuaca ekstrem di wilayah pesisir.", "Program mencakup pelatihan, penyusunan jalur evakuasi, dan penguatan kelembagaan siaga bencana di tingkat kampung.", "photo-1502082553048-f009c37129b9"),
    ("Jaringan Internet & Telekomunikasi", "berjalan", 45, 2026, "Peningkatan akses internet untuk mendukung layanan kampung dan belajar siswa.", "Perluasan jaringan bertujuan menghubungkan warga dan siswa dengan layanan digital serta informasi.", "photo-1507525428034-b723cf961d3e"),
    ("Dermaga / Pelabuhan Rakyat", "direncanakan", 20, 2027, "Sarana tambat perahu untuk memperlancar transportasi laut dan aktivitas nelayan.", "Dermaga rakyat direncanakan untuk memperlancar transportasi laut, kegiatan nelayan, dan kunjungan wisata melalui jalur laut.", "photo-1544551763-46a013bb70d5"),
]


class Command(BaseCommand):
    help = "Seed the database with sample village content (idempotent)."

    def handle(self, *args, **options):
        for order, (label, value) in enumerate(STATISTICS):
            Statistic.objects.update_or_create(label=label, defaults={"value": value, "order": order})

        for order, (title, subtitle, caption, photo) in enumerate(HERO_SLIDES):
            HeroSlide.objects.update_or_create(
                title=title,
                defaults={"subtitle": subtitle, "caption": caption, "image_url": img(photo), "order": order},
            )

        for order, (group, position, name, description) in enumerate(POSITIONS):
            OfficialPosition.objects.update_or_create(
                position=position,
                defaults={"group": group, "name": name, "description": description, "order": order},
            )

        for name, category, summary, description, photo in DESTINATIONS:
            Destination.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "category": category, "summary": summary, "description": to_html(description), "image_url": img(photo)},
            )

        for name, category, producer, summary, price_note, description, photo in PRODUCTS:
            Product.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name, "category": category, "producer": producer, "summary": summary, "price_note": price_note, "description": to_html(description), "image_url": img(photo)},
            )

        for order, (name, icon, summary) in enumerate(TRADITIONS):
            Tradition.objects.update_or_create(
                name=name, defaults={"icon": icon, "summary": summary, "order": order}
            )

        for title, category, date, photo, summary, body in POSTS:
            Post.objects.update_or_create(
                slug=slugify(title),
                defaults={"title": title, "category": category, "published_at": date, "image_url": img(photo), "summary": summary, "body": to_html(body)},
            )

        for title, category, date, location, summary in EVENTS:
            Event.objects.update_or_create(
                slug=slugify(title),
                defaults={"title": title, "category": category, "start_date": date, "location": location, "summary": summary},
            )

        for order, (title, photo) in enumerate(PHOTOS):
            Photo.objects.update_or_create(
                title=title, defaults={"image_url": img(photo), "order": order}
            )

        for title, status, progress, year, summary, description, photo in PROJECTS:
            Project.objects.update_or_create(
                slug=slugify(title),
                defaults={"title": title, "status": status, "progress": progress, "year": year, "summary": summary, "description": to_html(description), "image_url": img(photo)},
            )

        self.stdout.write(self.style.SUCCESS("Seed selesai."))
