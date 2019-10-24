from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, HashTag, Comment
from django.core.paginator import Paginator
from accounts.models import User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 4)  # 한 페이지에 몇개를 보여줄지

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
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


def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request, instance=post)
        if form.is_valid():
            post = form.save()
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#'):
                    hashtag = HashTag.objects.get_or_create(content=word)[0]
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)


def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('posts:index')


def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)
    posts = hashtag.taged_post.all()
    paginator = Paginator(posts, 4)  # 한 페이지에 몇개를 보여줄지

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)


def like(request, id):
    you = get_object_or_404(Post, id=id)
    me = request.user

    if me != you.user:
        if me in you.like_users.all():
            you.like_users.remove(me)
        else:
            you.like_users.add(me)

    return redirect('posts:index')


def comment_create(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.post = post
            comment_form.comment_user = request.user
            comment_form.save()
            return redirect('posts:index')


def comment_delete(request, p_id, c_id):
    comment = get_object_or_404(Comment, id=c_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('posts:index')
