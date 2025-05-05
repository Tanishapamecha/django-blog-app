# -------------------- IMPORTS --------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q


from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, ProfileForm, UserProfileForm

# DRF Imports
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# -------------------- AUTH VIEWS --------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('home')

# -------------------- HOME & POSTS --------------------
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

# @login_required
# def post_list(request):
#     posts = Post.objects.all().order_by('-created_at')
#     paginator = Paginator(posts, 5)  # 5 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     comment_forms = {post.id: CommentForm() for post in posts}
#     return render(request, 'blog/post_list.html', {'posts': posts, 'comment_forms': comment_forms})



# @login_required
# def post_list(request):
#     all_posts = Post.objects.all().order_by('-created_at')
#     paginator = Paginator(all_posts, 5)  # 5 posts per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     # Keep using 'posts' in the template
#     posts = page_obj.object_list
#     comment_forms = {post.id: CommentForm() for post in posts}

#     return render(request, 'blog/post_list.html', {
#         'posts': posts,            
#         'page_obj': page_obj,      
#         'comment_forms': comment_forms
#     })

@login_required
def post_list(request):
    query = request.GET.get('q', '')  # Get the search query from GET parameters

    # If a query exists, filter posts by title or content
    all_posts = Post.objects.all().order_by('-created_at')  # Get all posts ordered by creation date

    if query:
        # Filter posts by title or content if a query is provided
        all_posts = all_posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    paginator = Paginator(all_posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Keep using 'posts' in the template
    posts = page_obj.object_list
    comment_forms = {post.id: CommentForm() for post in posts}

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'page_obj': page_obj,
        'comment_forms': comment_forms,
        'query': query,  # Pass the search query to the template for persistence
    })



@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Automatically set the author
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'post': post})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Handle the comment form submission
    if request.method == "POST":
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user  # Set the author as the logged-in user
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')  # Redirect to login if user is not authenticated
    else:
        comment_form = CommentForm()

    # Fetch all comments for the post
    comments = post.comments.all()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

# -------------------- PROFILE --------------------
@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    editing = request.GET.get('edit') == 'true'

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/profile.html', {'form': form, 'profile': profile, 'editing': editing})

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_edit.html', {'form': form})

# -------------------- COMMENTS --------------------
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})

# -------------------- POST LIKE --------------------
@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)

# -------------------- DRF API VIEWS --------------------
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        # Automatically set the author of the comment to the logged-in user
        serializer.save(post=post, author=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
