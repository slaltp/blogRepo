from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.models import User
from .forms import LoginForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

class RegisterView(View):
    def get(self, request):
        regiForm = ProfileForm()
        return render(request, 'register.html', {'viewForm': regiForm})
    
    def post(self, request):
        regiForm = ProfileForm(request.POST)
        if regiForm.is_valid():
            password = regiForm.cleaned_data['password']
            password1 = regiForm.cleaned_data['password1']

            if password == password1:
                user = User.objects.create_user(
                    username = regiForm.cleaned_data['username'],
                    first_name = regiForm.cleaned_data['first_name'],
                    last_name = regiForm.cleaned_data['last_name'],
                    email = regiForm.cleaned_data['email'],
                    password = password)

                customer = regiForm.save(commit=False)
                customer.user = user
                customer.save()
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
            else:
                regiForm.add_error('password1', 'Passwords do not match.')
        return render(request, 'register.html', {'viewForm': regiForm})

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'home.html', {'user': user})
class CreatePost(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'home.html', {'form': form})
    
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            createdPost = form.save(commit=False)
            createdPost.author = request.user
            createdPost.save()
            return redirect('index')
        else: 
            return render(request, 'home.html', {'form': createdPost})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace with your actual home view name
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})

#def postRead(request, id):
#    post = Post.objects.get(id = id)
#    return render(request, 'posts.html',{'posts': post})

@login_required
def postRead(request, id):
    post = Post.objects.get(id = id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts', id = id)
    else:
        form = CommentForm()

    return render(request, 'posts.html', {'posts': post, 'comments': comments, 'form': form})

class PostCreatedbyUsser(LoginRequiredMixin,View):
    def get(self, request):
        ownPost = Post.objects.filter(author = request.user)
        return render(request, 'posts.html', {'ownPost': ownPost})

@login_required
def postDelete(request, id):
    post = get_object_or_404(Post, id = id)
    if post.author == request.user:
        post.delete()
        return redirect('index')

@login_required  
def postEdit(request, id):
    post = get_object_or_404(Post, id = id)
    if post.author == request.user:
        editForm = PostForm(instance=post)
        return render(request, 'home.html', {'form': editForm})

