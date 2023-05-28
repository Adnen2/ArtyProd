from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment, Profile, Category
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def post_list(request):
    posts = Post.objects.annotate(num_comments=Count('comments'))
    categories = Category.objects.all()
    profile=Profile.objects.get(user=request.user)
    post_form = None

    if request.method == 'POST':
        if request.user.is_authenticated:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                content = post_form.cleaned_data['content']
                image = post_form.cleaned_data['image']
                author = request.user
                post = Post.objects.create(content=content, image=image, author=author)
                return redirect('/BlogApplication/')
    else:
        post_form = PostForm()

    context = {
        'posts': posts,
        'profile':profile,
        'categories': categories,
        'post_form': post_form
    }
    return render(request, 'post_list.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()
    profile=Profile.objects.get(user=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_content = comment_form.cleaned_data['comment']
            author = Profile.objects.get(user=request.user)
            Comment.objects.create(post=post, author=author, content=comment_content)
            return redirect('BlogApplication:post_detail', post_id=post_id)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'profile':profile
    }
    return render(request, 'post_detail.html', context)

def search(request):
    query = request.GET.get('q')
    profile=Profile.objects.get(user=request.user)
    categories = Category.objects.all()
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.none()  # Return an empty queryset if no query is provided

    context = {
        'posts': posts,
        'query': query,
        'categories': categories,
        'profile':profile
    }
    return render(request, 'search.html', context)
