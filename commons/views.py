from django.utils import timezone
from django.views.generic import TemplateView

from culture.models import Tradition
from events.models import Event
from news.models import Post
from tourism.models import Destination

from .models import ContactChannel, FastFact, HeroSlide, MissionPoint, OfficialPosition, Statistic


class HomeView(TemplateView):
    template_name = "commons/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hero_slides"] = [
            {
                "img": s.image.url if s.image else "https://dummyimage.com/1600x1000",
                "fb": "https://dummyimage.com/1600x1000",
                "title": s.title,
                "sub": s.subtitle,
                "caption": s.caption,
            }
            for s in HeroSlide.objects.filter(is_published=True)
        ]
        context["statistics"] = Statistic.objects.filter(is_published=True)
        context["posts"] = Post.objects.filter(is_published=True)[:3]
        context["destinations"] = Destination.objects.filter(is_published=True)[:6]
        context["events"] = Event.objects.filter(
            is_published=True, start_date__gte=timezone.now().date()
        )[:3]
        context["kepala_kampung"] = OfficialPosition.objects.filter(
            position__iexact="Kepala Kampung", is_published=True
        ).first()
        return context


class AboutView(TemplateView):
    template_name = "commons/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        positions = OfficialPosition.objects.filter(is_published=True)
        context["gov_positions"] = positions.exclude(group=OfficialPosition.Group.CUSTOM)
        context["adat_institutions"] = positions.filter(group=OfficialPosition.Group.CUSTOM)
        context["traditions"] = Tradition.objects.filter(is_published=True)
        context["quick_facts"] = FastFact.objects.filter(group=FastFact.Group.QUICK_FACTS)
        context["boundaries"] = FastFact.objects.filter(group=FastFact.Group.BOUNDARIES)
        context["mission_points"] = MissionPoint.objects.all()
        return context


class ContactView(TemplateView):
    template_name = "commons/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_channels"] = ContactChannel.objects.all()
        return context


class StatisticsView(TemplateView):
    template_name = "commons/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statistics"] = Statistic.objects.filter(is_published=True)
        return context
