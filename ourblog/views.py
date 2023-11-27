from typing import Any
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm, EditForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect 
# def home(request):
  #   return render(request, 'home.html', {})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name ='home.html'
    ordering = ['-post_date']

class ArticleDetailView(DetailView): 
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        total_dislikes = stuff.total_dislikes()
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context["total_likes"] = total_likes
        context['total_dislikes'] = total_dislikes
        return context
    


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    #fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'

    def form_valid(self, form):
        # Set updated_date only when the form is valid and the post is being updated
        if self.object.update_date:
            form.instance.update_date = None  # Clear updated_date to trigger save
        return super().form_valid(form)


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')