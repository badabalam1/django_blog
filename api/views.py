from .forms import PostForm, CommentForm
from .models import Post
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Post, Comment


def tagstring_to_taglist_in_post(post):

    post.tags = map(lambda tag: tag.strip(), post.tags.split(','))
    return post

# Create your views here.


def index(request):
    return HttpResponse('asdf')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', pk=pk)

    post = tagstring_to_taglist_in_post(post)
    form = CommentForm()
    comments = Comment.objects.filter(post=post.pk).order_by('created_at')
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})


def post_list(request):
    page = int(request.GET['page']) if 'page' in request.GET.keys() else 1
    tag = request.GET['tag'] if 'tag' in request.GET.keys() else ''

    posts = Post.objects.order_by('-created_at')
    length = len(posts)
    posts = posts.filter(tags__contains=tag) if tag else posts
    posts = posts[(page - 1) * 10:page * 10]
    posts = list(map(tagstring_to_taglist_in_post, posts))
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'page': page,
        'tag': tag,
        'length_page': page * 10,
        'length': length
    })


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # instance : 수정할 qs를 넣어준다.
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            edit_post = form.save(commit=False)
            edit_post.save()

            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('list')


def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


def Login(request):
    return render(request, 'registration/login.html')


def Logout(request):
    logout(request)
    return redirect('login')
    # return render(request, 'registration/logged_out.html')
