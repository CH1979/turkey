from django.contrib import admin

from .models import Article, Rubric


admin.site.register(Rubric)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article

    def get_fields(self, request, object=None):
        fields = [
            'title',
            'cover',
            'rubric',
            'author',
            'content',
            'tags',
        ]
        if request.user.is_superuser:
            fields.append('is_draft')
        return fields
