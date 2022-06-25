from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Link, Article, Headline, Tag
from django.db.models import Max
from .forms import ArticleForm
import random
from django.contrib.auth.decorators import login_required

def news(request):
    #links = reversed(Link.objects.all())
    arts = (Article.objects.filter(published=True).order_by('-date'))
    headline = Headline.objects.all().order_by('-id')
    links = headline[1:5]


    return render(request, 'news.html', {'headline':headline[0],'links':links, 'arts':arts})

@login_required
def NewArticle(request):
    if request.method == 'GET':
        form = ArticleForm()
        return render(request, "ArticleForm.html", {'form': form})
    elif request.method == 'POST':
        form = ArticleForm(request.POST)
        msg="... ? ..."
        try:
            tlen = len(form['text'].data)
        except:
            
            return render(request, "ArticleForm.html", {'form': form, 'msg': msg})

        return render(request, "ArticleForm.html", {'form': form, 'msg': msg})

@login_required
def ArticleSubmit(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.POST
            files = request.FILES
            article = Article()
            article.url=(data['title']).replace(" " or "%20", "-")
            article.text=data['text']
            article.title=data['title']
            article.author=request.user
            article.image=files.get('image')
            if "default_bg" in request.POST:
                article.bg_img = 'articles/default_bg.png'
                article.bg_color='#00000000'
            else: 
                article.bg_img=files.get('bg_img')
                article.bg_color=data['bg_color']
            article.save()

            try: 
                tags = data['tags'].strip()
                tlist = tags.split(',')
                for t in tlist:
                    this_tag = Tag.objects.get_or_create(name=t)
                    article.tags.add(this_tag)
            except:
                pass
        
            return HttpResponse('Success!')
        return HttpResponse('Invalid Form')
    return HttpResponse('Failure.')

def ArticleView(request, username, article):
    try:
        art = Article.objects.get(url=article, author__username=username)
        return render(request, 'ArticleView.html', {'art':art})
    except:
        msg = 'Sorry, that article does not exist.'
        return redirect('/@'+username)