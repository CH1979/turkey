from cgitb import text
from haystack import indexes

from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document= True,
        use_template=True,
    )
    author = indexes.CharField(
        model_attr='author'
    )

    def get_model(self):
        return Article
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_draft=False)
