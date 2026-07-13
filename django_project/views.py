from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /site-manager/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
