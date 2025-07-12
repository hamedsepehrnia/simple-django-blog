from django.urls import path

from auth_app import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('edit-info/', views.edit_profile ,name='edit_info'),
    path('profile/<username>', views.profile, name='profile'),
]