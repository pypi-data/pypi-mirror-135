from django.views.generic import TemplateView


class AppView(TemplateView):
    template_name = 'app/index.html'


class SectionView(TemplateView):
    template_name = 'app/section.html'
