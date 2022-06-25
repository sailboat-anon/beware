from django.db import models
from django.conf import settings


class Cipher(models.Model):
    name = models.CharField(max_length=74)
    color = models.CharField(max_length=12)

    @property
    def symbols(self):
        return Symbol.objects.filter(cipher=self)

    def __str__(self):
        return self.name


class Symbol(models.Model):
    char = models.CharField(max_length=1)
    value = models.IntegerField()
    cipher = models.ForeignKey(Cipher, on_delete=models.CASCADE)

    def __str__(self):
        return self.char + " " + self.cipher.name


class Value(models.Model):
    num = models.IntegerField()
    ciph = models.ForeignKey(Cipher, on_delete=models.CASCADE)

    @property
    def selfstr(self):
        return "" + str(self.num) + " " + str(self.ciph.name)

    def __str__(self):
        return "" + str(self.num) + " " + str(self.ciph.name)


class Phrase(models.Model):
    text = models.TextField(max_length=None)
    values = models.ManyToManyField(Value)

    @property
    def searches(self):
        return Search.objects.filter(phrase=self).count()

    def __str__(self):
        return self.text


class Search(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    ip = models.CharField(max_length=25, blank=True)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip + self.phrase.text
    #TODO make searches property on user profile model and IP

class Post(models.Model):
    content = models.TextField(max_length=None, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    values = models.ManyToManyField(Value)
    cipher = models.ForeignKey(Cipher, on_delete=models.CASCADE, default=None, blank=True, null=True)
    #link = models.URLField(blank=True)
    replies = models.ManyToManyField("self", blank=True, related_name="thread", default=None)

    @property
    def parent(self):
        filt = Post.objects.filter(replies=self)
        if filt.count() >= 1:
            for n in Post.objects.filter(replies=self):
                if n.date < self.date:
                    return n
        else:
            return None

    @property
    def comments(self):
        num = self.replies.count()
        if self.parent:
            num = num-1
        return num

    @property
    def votes(self):
        return Vote.objects.filter(post=self)

    @property
    def score(self):
        return Vote.objects.filter(post=self, value=True).count() - Vote.objects.filter(post=self, value=False).count()
    
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.BooleanField(default=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)