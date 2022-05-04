from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from taggit.models import Tag

from .models import Article, Rubric


class ArticleMainView(TemplateView):
    """Представление главной страницы раздела Статьи"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['last_articles'] = Article.objects.all()[:4]

        groupped_articles = dict()
        rubrics = Rubric.objects.filter(on_main=True)
        for rubric in rubrics:
            groupped_articles[rubric] = Article.objects \
                .filter(is_draft=False) \
                .filter(rubric=rubric)[:4]
        context['groupped_articles'] = groupped_articles

        context['tags'] = Tag.objects.all()
        return context


class ArticleDetailView(DetailView):
    """Представление одной статьи"""
    model = Article


class ArticlesByRubricView(ListView):
    """Представление списка статей фильтр по категории"""
    model = Article
    template_name = 'articles/articles_by_rubric.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = Rubric.objects.get(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = super().get_queryset()
        return queryset.filter(rubric_id=pk)


class ArticlesByTagView(ListView):
    """Представление списка статей фильтр по тегу"""
    model = Article
    template_name = 'articles/articles_by_tag.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = super().get_queryset()
        return queryset.filter(tags__id__in=[pk])
