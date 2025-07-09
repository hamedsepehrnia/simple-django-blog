from django.http import HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import comment
from pyexpat.errors import messages
from django.db.models import Count

from Messages_app.models import Message
from articles_app.models import Article, Category, Comment
from django.core.paginator import Paginator

def home(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, "home_app/index.html", context)
def about(request):
    return render(request, "home_app/about.html")
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = request.POST.get("subject")
        Message.objects.create(name=name, email=email, message=message, subject=subject)
    return render(request, "home_app/contact.html")

def details(request, slug):
    articles = Article.objects.all()
    if not articles.exists():
        return HttpResponse('no articles yet')
    if slug != ' ':
        article = Article.objects.get(slug=slug)
        if request.method == 'POST':
            content = request.POST['content']
            parent_id = request.POST['parent_id']
            Comment.objects.create(article=article, content=content, parent_id=parent_id, user=request.user)
        context = {'article': article, 'parent_id': request.POST.get('parent_id') or None}
        return render(request, "home_app/post-details.html", context)
    elif slug == ' ':
        article = Article.objects.latest('published_date')
        if request.method == 'POST':
            content = request.POST['content']
            parent_id = request.POST['parent_id']
            Comment.objects.create(article=article, content=content, parent_id=parent_id, user=request.user)
        context = {'article': article, 'parent_id': request.POST.get('parent_id')}
        return render(request, "home_app/post-details.html", context)

def profile(request, username):
    user = User.objects.get(username=username)
    context = {'user': user}
    return render(request, "home_app/profile.html", context)
def blog(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 8)
    page_number = request.GET.get('page')
    objects = paginator.get_page(page_number)
    context = {'articles': objects}
    return render(request, "home_app/blog.html", context)
def category_details(request, cat_id):
    category = get_object_or_404(Category, id = cat_id)
    articles = category.articles.all()
    context = {'articles': articles}
    return render(request, 'home_app/blog.html', context)