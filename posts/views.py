from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .utils import post_create

@login_required
def new_post(request):
    context = []
    if request.method == 'POST':
        form = request.POST
        content = form['content']
        cipher = form['cipher']
        user = request.user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        if form['content'].strip() == "":
            return redirect('home')  
        else:
            try:
                parent = form['parent']
            except:
                parent = "0"
            status = post_create(cipher, content, user, ip, parent)
            
            print(status)
            return redirect('home')
    else:
        return redirect('home')

@login_required
def vote(request):
    if request.method == 'POST':
        form = request.POST
        postID = form['number']
        post = Post.objects.get(id=postID)
        value = bool
        if form['value'] == 'True':
            value = True
        elif form['value'] == 'False':
            value = False
        
        user = request.user
        vote, made = Vote.objects.get_or_create(user=request.user,post=post)
        print(value)
        if made:
            this_vote = Vote.objects.get(user=request.user,post=post) 
            this_vote.value = value
            this_vote.save()
            print('new')
            return HttpResponse('new')
        else:
            this_vote = Vote.objects.get(user=request.user,post=post) 
            if this_vote.value == value:
                this_vote.delete()
                print('revoked')
                return HttpResponse('revoked')
            else:
                print(this_vote.value)
                this_vote.value = value
                this_vote.save()
                print('changed')
                return HttpResponse('changed')
            
    else:
        return HttpResponse('failure')

def post_view(request, post_id):
    post = Post.objects.get(id=post_id)

    return render(request, 'Post.html', {'post': post})