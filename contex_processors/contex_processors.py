from articles_app.models import Article, Category


def recent_articles(request):
    ordered_articles = Article.objects.order_by('-published_date')[:3]
    categories = Category.objects.all()
    return {'ordered_articles': ordered_articles, 'categories': categories}