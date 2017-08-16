from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (TemplateView,
                                    ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView,)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
# Create your views here.

class AboutView(TemplateView):
     template_name = 'about.html'


class PostListView(ListView):
    model = Post
    #Prikazacemo postove samo one koji su pre trenutnog datuma objavljeni.
    def get_queryset(self):
        #Uzmi sve postove i filtriraj ih da su svi mladji (__lte) ili jednaki od timezone.now() i onda ih poredjaj po published_date
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        #prevodi direktno SQL proveri dokumentaciju Field lookups u Django

class PostDetailView(DetailView):
    model = Post

#LoginRequiredMixin ista stvar kao i login sa dekoratorima, ali samo za CBV
class CreatePostView(LoginRequiredMixin, CreateView):
    #Kada se osoba uloguje gde treba da ide link ispod.
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    #Kada se osoba uloguje gde treba da ide link ispod.
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    #konektujes se na model iz kojeg zelis da brises stavke
    model = Post
    #zelim nakon sto obrisem post da se vratim na pocetnu stranu
    #Dakle, parametar reverse_lazy bice post_list jer:
    #url(r'^$',views.PostListView.as_view(),name='post_list'),
    success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        #kad izvucem listu postova, zelim da proverim da oni nemaju published_date
        #Na taj nacin znam da izlistavam postove koji nisu objavljeni (ustvari Draftovi)
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


################################################################################
############# Function based views (FBV) - Logika za komentare   ###############
################################################################################

#trazimo da bi se izvrsila ova metoda da korisnik bude ulogovan
@login_required
def add_comment_to_post(request,pk):
    #uzmi taj objekat ili idi na 404 stranicu
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
            form = CommentForm()
    return render(request, 'blog/comment_form.html',{'form': form})

#trazimo da bi se izvrsila ova funckcija da korisnik bude ulogovan
@login_required
def comment_approve(request,pk):
    #comment = CommentForm(request.POST)
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    #vrati me na stranicu potrazi u Comment Primary Key pa posle toga u Post
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    #moramo da snimimo Primary key za post, posto kada u sledecem koraku
    #izbrisemo Post, vise necemo moci da znamo koji broj posta je to bio
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post= get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_list')
