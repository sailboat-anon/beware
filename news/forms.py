from django import forms
from django.forms.widgets import TextInput
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
            model = Article
            exclude = ('bg_img', 'author','is_read_only', 'date', 'published','url','tags')
            widgets = {
                'text': SummernoteWidget(),
                'bg_color': forms.TextInput(attrs={'type': 'color'}),
            }
            labels = {
                'text' : '',
                'image': 'Cover Image',
                #'bg_img': 'Background Image',
                'bg_color': 'Background Color',
            }