from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('search'), permanent=True)),
    path('wiki/', include('wiki.urls')),
    path('admin/', admin.site.urls),
]
