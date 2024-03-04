from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('feed/', views.feed_view, name='feed'),
    path('search-results/', views.search_results_view, name='search_results')
]
