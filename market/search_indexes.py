import datetime

from haystack import indexes

from .models import Lot


class LotIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
    )
    author = indexes.CharField(
        model_attr='author'
    )

    def get_model(self):
        return Lot
