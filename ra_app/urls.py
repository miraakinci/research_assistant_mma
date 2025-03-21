from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_or_feed, name="home_or_feed"),
    path('home/', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('save-paper/', views.save_paper_view, name='save_paper'),
    path('unsave-paper/<int:paper_id>/', views.unsave_paper_view, name='unsave_paper'),
    path('library/', views.display_paper_view, name='library'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('feed/', views.feed_view, name='feed'),
    path('search-results/', views.search_results_view, name='search_results'),
    path('code-of-conduct/', views.code_of_conduct_view, name='code_of_conduct'),
]
