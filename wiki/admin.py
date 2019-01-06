from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Page, Tag


class PageAdmin(admin.ModelAdmin):
    list_display = ("name", "show_link",)
    search_fields = ("tags__text",)
    filter_horizontal = ("tags",)

    def show_link(self, obj):
        return mark_safe('<a target=blank href="%s">%s</a>' % (obj.link, obj.link))


admin.site.register(Page, PageAdmin)
admin.site.register(Tag)
