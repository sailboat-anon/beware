from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass

@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

class SummerNoteAdmin(SummernoteModelAdmin):
    summernote_fields = 'text'

admin.site.register(Article, SummerNoteAdmin)