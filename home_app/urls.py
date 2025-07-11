from django.urls import path

from home_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('details/<str:slug>', views.details, name='details'),
    path('details/ ', views.details, name='details'),
    path('profile/<username>', views.profile, name='profile'),
    path('blog/', views.blog, name='blog'),
    path('category-details/<int:cat_id>', views.category_details, name='category_details'),
]