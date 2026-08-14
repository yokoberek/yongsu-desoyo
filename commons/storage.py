from django.conf import settings
from django.core.files.storage import FileSystemStorage


class EditorImageStorage(FileSystemStorage):
    """Gambar yang di-upload dari dalam editor.

    django-ckeditor-5 menyimpan file dengan nama aslinya di root storage, jadi
    storage ini diarahkan ke sub-folder sendiri agar tidak tercampur dengan
    media milik model (news/, gallery/, dst).
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", settings.MEDIA_ROOT / "editor")
        kwargs.setdefault("base_url", f"{settings.MEDIA_URL}editor/")
        super().__init__(*args, **kwargs)
