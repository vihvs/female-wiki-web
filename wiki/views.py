from django.views.generic.list import ListView
from django.views.generic import TemplateView

from wiki.models import Page

class PageListView(ListView):

    model = Page

    def get_queryset(self):
        tags = self.request.GET['tags'].replace(" ","").split(',')
        print(tags)
        queryset = super().get_queryset()
        for tag in tags:
            queryset = queryset.filter(tags__text__icontains=tag)
        return queryset[:30]

class SearchView(TemplateView):
     template_name = "wiki/search.html"