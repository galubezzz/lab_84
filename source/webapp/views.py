from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article, Comment
from django.shortcuts import get_object_or_404


class ArticleListView(ListView):
    template_name = 'article_list.html'
    model = Article


class ArticleDetailView(DetailView):
    template_name = 'article_detail.html'
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article_create.html'
    form_class = ArticleForm
    model = Article

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'article_update.html'
    form_class = ArticleForm
    model = Article

    def get_permission_required(self):
        return None

    def has_permission(self):
        return self.request.user == self.get_object().author


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'partial/comment_form.html'
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.request.article_id)
        form.instance.article = article
        form.instance.author = self.request.user
        return super(CommentCreateView, self).form_valid(form)

