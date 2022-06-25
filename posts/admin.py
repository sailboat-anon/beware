from django.contrib import admin
from .models import *


class SymbolAdmin(admin.StackedInline):
    model = Symbol

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content']

@admin.register(Cipher)
class CipherAdmin(admin.ModelAdmin):
    inlines = [SymbolAdmin]
    list_display = ['name', 'color']

@admin.register(Symbol)
class SymbolAdmin(admin.ModelAdmin):
    list_display = ['char', 'value', 'cipher']
    
@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ['selfstr']

@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ['text', 'searches']

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip', 'phrase', 'date']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user']