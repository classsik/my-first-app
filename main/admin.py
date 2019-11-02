from django.contrib import admin
from .models import News, Shedule

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'published')
admin.site.register(News, NewsAdmin)
admin.site.register(Shedule)
