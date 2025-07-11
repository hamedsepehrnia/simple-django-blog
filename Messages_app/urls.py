from Messages_app import views
from django.urls import path
urlpatterns = [
    path('contact', views.contact, name='contact'),
]