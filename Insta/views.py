from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView

from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.urls import reverse, reverse_lazy

from Insta.forms import CustomUserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin

from annoying.decorators import ajax_request

from Insta.models import Post, Like

class HelloWorld(TemplateView):
    # overwrite the template_name
    template_name = 'test.html'


class PostsView(ListView):
    # generate a list of object where each object is a Post model
    model = Post
    # pass the Post model to index.html
    template_name = 'index.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']
    

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url  = reverse_lazy("posts")



class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')


# because it is an ajax request, it does not have to be a template view
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    # because the existing of like, it now cancelles previous likes
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }