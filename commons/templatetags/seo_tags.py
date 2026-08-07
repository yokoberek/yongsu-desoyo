from django import template

from commons.models import PageBanner

register = template.Library()


@register.simple_tag
def banner_image(key, fallback=""):
    """Image for a partials/page_banner.html slot, picked via admin (PageBanner) from
    Galeri Foto; falls back to the given URL when no key is set up yet or no photo is chosen."""
    banner = PageBanner.objects.filter(key=key).select_related("photo").first()
    if banner and banner.photo:
        return banner.photo.image.url
    return fallback


@register.tag(name="captureas")
def do_captureas(parser, token):
    """Render a block into a context variable so its output can be reused in
    multiple places (e.g. the same title text in <title>, og:title, and
    twitter:title) without duplicating the block itself — Django forbids a
    {% block %} name from appearing more than once per template.

    Usage: {% captureas var_name %}...{% endcaptureas %}
    """
    try:
        _, variable_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("captureas tag requires exactly one argument")
    nodelist = parser.parse(("endcaptureas",))
    parser.delete_first_token()
    return CaptureasNode(nodelist, variable_name)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, variable_name):
        self.nodelist = nodelist
        self.variable_name = variable_name

    def render(self, context):
        # Render normally (autoescape untouched) so any {{ variable }} inside the
        # block is escaped exactly once, here. NodeList.render() always returns a
        # SafeString, so re-emitting the captured value later via {{ var }} does
        # not escape it a second time — this mirrors how {{ block.super }} works.
        output = self.nodelist.render(context)
        context[self.variable_name] = output
        return ""
