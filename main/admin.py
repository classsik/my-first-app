from django.contrib import admin
from .models import News, Shedule, Comment, Call

def deactivate(self, request, queryset):
    queryset.update(active='False')
deactivate.short_description = "Не показывать"

def activate(self, request, queryset):
    queryset.update(active='True')
activate.short_description = "Показывать"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'news', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')
    actions = [deactivate, activate]

admin.site.register(Comment, CommentAdmin)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'body', 'published')
admin.site.register(News, NewsAdmin)
admin.site.register(Shedule)
admin.site.register(Call)
