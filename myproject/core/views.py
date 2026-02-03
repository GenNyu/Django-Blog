from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .models import Post
from .forms import PostForm

def home(request):
    posts = Post.objects.all()
    return render(request, 'core/home.html', {
        'posts': posts,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'core/create_post.html', {
        'form': form,
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'core/post_detail.html', {
        'post': post,
    })


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-id')
    return render(request, 'core/my_posts.html', {'posts': posts})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'core/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'core/confirm_delete.html', {'post': post})

class LoginViewWithMessage(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get(self.redirect_field_name)
        if next_url == reverse('create_post'):
            messages.warning(request, "Bạn cần đăng nhập để tạo bài viết.")
        return super().get(request, *args, **kwargs)
