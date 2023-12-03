from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Articles, ArticleCategory, ArticleComments
from django.http import HttpResponse, HttpRequest


#------------------------------------------------------------------------
# to load articles and filter them by category
class ArticlesView(ListView):
    template_name = 'articles.html'
    model = Articles
    paginate_by = 3
    context_object_name = 'articles'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(categories__url_title__iexact=category_name, is_active=True)
        return query


#------------------------------------------------------------------------
# to load side-bar (categories)
def article_categories_component(request):
    categories = ArticleCategory.objects.filter(is_active=True, parent_category=None)
    context = {'categories': categories}
    return render(request, 'components/article_categories_component.html', context)


#------------------------------------------------------------------------
# to load article detail page
class ArticleDetailView(DetailView):
    template_name = 'article_detail.html'
    model = Articles
    context_object_name = 'article'

# to check if article is_active :
    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query

# to get comments :
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article: Articles = kwargs.get('object')
        context['comments'] = ArticleComments.objects.filter(article_id=article.id, is_active=True, parent=None).prefetch_related('articlecomments_set').order_by('-create_date')
        context['comments_count'] = ArticleComments.objects.filter(article_id=article.id, is_active=True).count()
        return context


#------------------------------------------------------------------------
# to save comments in db
def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        ArticleComments.objects.create(
            article_id=article_id,
            parent_id=parent_id,
            user_id=request.user.id,
            text=article_comment,
            is_active=True

        )
    return HttpResponse('end of function')
