from django.contrib import admin
from .models import Category, Tag, Code

class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Code, CodeAdmin)