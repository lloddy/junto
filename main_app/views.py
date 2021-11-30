from django.http.response import  HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from django.urls import reverse_lazy






# Define the home view
def home(request):
  return render(request, 'home.html')

@login_required
def posts_index(request):
  posts = Post.objects.all()
  
  return render(request, 'posts/index.html', { 'posts': posts })

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'posts/profile.html', { 'posts': posts })

@login_required
def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    user_form = UserForm()

    return render(
        request, 
        'posts/detail.html', { 
            'post': post,
            'user_form': user_form,
        })

def get_context_data(self, *args, **kwargs):
    context=super(posts_detail, self).get_context_data
    stuff=get_object_or_404(Post, id=self.kwargs['post_id'])
    total_likes=stuff.total_likes()
    context['total_likes']=total_likes
    return context


def add_category(request, post_id):
    form = UserForm(request.POST)
    print(form._errors)
    if form.is_valid():
        new_category = form.save(commit=False)
        new_category.post_id = post_id
        new_category.save()

    return redirect('detail', post_id=post_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def LikeView(request, post_id):
    post= get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return redirect('index')

class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user  # form.instance is the cat
    return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = '__all__'

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts/'