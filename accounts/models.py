from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, verbose_name="Display Name")
    text_color = models.CharField(max_length=12, blank=True, default='#FFFFFF')
    accent_color = models.CharField(max_length=12, blank=True, default='#AAAAAA')
    bg = models.URLField(blank=True, verbose_name='Background tile Image URL', default="/static/bg.png")
    image = models.URLField(blank=True, verbose_name="Header Image URL", default="/static/surveillance.png" )
    photo = models.URLField(blank=True, verbose_name="Profile Picture URL", default="/static/defaultuser.png")
    bio = models.CharField(max_length=228, verbose_name='About', blank=True)
    website = models.URLField(max_length=100, verbose_name='Your Website', blank=True)
    phone = models.CharField(max_length=14, verbose_name='Phone Number', blank=True)

    @property
    def posts(self):
        return Post.objects.filter(author=self.user)

    @property
    def followers(self):
        return Follow.objects.filter(follows=self.user) # try {{ user.profile.followers.count }} to get the number

    @property
    def following(self):
        return Follow.objects.filter(user=self.user) # try {{ user.profile.following.count }} to get the number (or |length)

    @property
    def settings(self):
        return Setting.objects.get(user=self.user)
    #TODO: follow numbers in a given cipher

    @property
    def ciphers(self):
        settings = Setting.objects.get(user=self.user)
        return settings.ciphers.all()


class Setting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ciphers = models.ManyToManyField('posts.Cipher', related_name="ciphers")
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=999999)