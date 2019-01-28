from django.views.generic.list import ListView
from django.views.generic import TemplateView

from wiki.models import Page

class PageListView(ListView):

    model = Page

    def get_queryset(self):
        tags = self.request.GET['tags'].split(',')
        queryset = super().get_queryset()
        return queryset.filter(tags__text__in=tags)[:30]

class SearchView(TemplateView):
     template_name = "wiki/search.html"