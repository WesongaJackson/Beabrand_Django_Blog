from django.shortcuts import get_object_or_404, render
from. models import Post,Comment
from django.contrib.auth.mixins import  LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,DeleteView
# Create your views here.


def home(request):
    posts=Post.objects.all()
    context={
        'posts':posts,
    }
    return render(request,'BlogApp/home.html',context)

class PostListView(ListView):
    model=Post
    template_name='BlogApp/home.html'
    context_object_name='posts'
    ordering=['-date_posted']

class PostDetailView(LoginRequiredMixin,DetailView):
    model=Post
    template_name='BlogApp/post_details.html'
    context_object_name='post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        context['comments'] = comments
        return context

    
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)




class CommentCreateView( LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)
    def get_success_url(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post.get_absolute_url()

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    context_object_name='post'
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Comment
    context_object_name='comment'
    def test_func(self):
        comment=self.get_object()
        if self.request.user==comment.author:
            return True
        return False  
    def get_success_url(self):
        comment = self.get_object()
        return comment.post.get_absolute_url() 

def about(request):
    return render(request,'BlogApp/about.html',{'title':'about'})
