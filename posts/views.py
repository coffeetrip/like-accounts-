from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, HashTag
# Create your views here.


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def create(request):
    if request.method == 'POST':
        # 이미지는 request.FILES로 받아야함
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # 로그인한사람 = 글쓰는 사람
            post.save()
            for word in post.content.split():
                if word.startswith('#'):  # #으로 시작하면
                    # hashtag 추가
                    # get_or_create 중복을 막아줌
                    # 2개의 데이터 나옴(튜플) -> (obj, True or False)
                    hashtag = HashTag.objects.get_or_create(content=word)[0]
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)


def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)
    posts = hashtag.taged_post.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def like(request, id):
    you = get_object_or_404(Post, id=id)
    me = request.user

    if me != you:
        if me in you.like_users.all():
            you.like_users.remove(me)
        else:
            you.like_users.add(me)

    return redirect('posts:index')
