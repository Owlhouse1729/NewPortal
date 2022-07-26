from django.shortcuts import render, redirect
from django.views.generic import *
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import *
from accounts.models import User
from .forms import CreateThreadForm


class Top(View):
    template_name = 'social/top.html'

    def get(self, request, *args, **kwargs):
        if 'genre_id' not in self.kwargs:
            return redirect('social:top', genre_id=1)
        genre_id = self.kwargs['genre_id']
        current_genre = get_object_or_404(Genre, genre_id=genre_id)
        genres = Genre.objects.all()
        threads = Thread.objects.filter(genre=current_genre).order_by('-last_update')

        params = {
            'current_genre': current_genre,
            'genres': genres,
            'threads': threads,
        }
        return render(request, self.template_name, params)


class ViewPosts(View):
    template_name = 'social/view_posts.html'

    def post(self, request, *args, **kwargs):
        current_thread_id = self.kwargs['thread_id']
        thread = Thread.objects.get(pk=current_thread_id)
        author = self.request.user
        content = self.request.POST['content']
        if content:
            date_posted = timezone.now()
            Post.objects.create(thread=thread, author=author, content=content, date_posted=date_posted)
            thread.last_update = timezone.now()
            thread.replies = Post.objects.filter(thread=thread).count()
            thread.save()
            return redirect('social:view_posts', thread_id=current_thread_id)
        else:
            return redirect('social:view_posts', thread_id=current_thread_id)

    def get(self, request, *args, **kwargs):
        thread_id = self.kwargs['thread_id']
        thread = Thread.objects.filter(pk=thread_id).get()
        current_genre = Thread.objects.filter(pk=thread_id).get().genre
        genres = Genre.objects.all()
        posts = Post.objects.filter(thread=Thread.objects.get(pk=thread_id)).order_by('date_posted')
        user_pk = self.request.user.pk
        user = User.objects.get(pk=user_pk)
        params = {
            'current_genre': current_genre,
            'genres': genres,
            'posts': posts,
            'user': user,
            'thread': thread,
        }
        return render(request, self.template_name, params)


class CreateThread(CreateView):
    model = Thread
    form_class = CreateThreadForm
    template_name = 'social/create_thread.html'
    # success_url = reverse_lazy('social:top')

    def form_valid(self, form):
        tmp = form.save(commit=False)
        tmp.owner = self.request.user
        tmp.date_created = timezone.now()
        tmp.last_update = timezone.now()
        tmp.save()
        return redirect('social:view_posts', thread_id=tmp.pk)
