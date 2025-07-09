from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.template.defaultfilters import title
from django.utils.timezone import now
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.db import models
from unicodedata import category

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='articles')
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    comments_count = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content





@receiver(post_save, sender=Comment)
def increment_comments_count(sender, instance, created, **kwargs):
    if created:
        Article.objects.filter(id=instance.article_id).update(comments_count=models.F('comments_count') + 1)

@receiver(post_delete, sender=Comment)
def decrement_comments_count(sender, instance, **kwargs):
    Article.objects.filter(id=instance.article_id).update(comments_count=models.F('comments_count') - 1)