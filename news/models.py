from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse

import re
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

class Link(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

class Headline(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField()
    description = models.TextField(blank=True)
    image = models.FileField(upload_to='headlines/', default='headlines/default.jpg', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def via(self):
        t = urlparse(self.link).netloc
        return "via " + ('.'.join(t.split('.')[1:]))

class Tag(models.Model):
    name = models.CharField(max_length=74)

    def __str__(self):
        return self.name

class Article(models.Model):
    url = models.CharField(max_length=154, default="")
    text = models.TextField(blank=False)
    title = models.CharField(max_length=228, default="")
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    tags = models.ManyToManyField(Tag, blank=True)
    published = models.BooleanField(default=False)
    image = models.FileField(upload_to='articles/', default="", blank=True, null=True)
    bg_img = models.FileField(upload_to='articles/', default="", blank=True, null=True)
    bg_color = models.CharField(max_length=9, default="#000000", blank=True)

    def __str__(self):
        return self.title

    @property
    def preview(self):
        ctext=cleanhtml(self.text)
        return ctext[0:100]