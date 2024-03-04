from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LogInForm, FavouritePaperForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import FavouritePaper
from .api import fetch_articles_from_google_scholar
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #user.refresh_from_db()
            user.newPassword = form.cleaned_data.get("newPassword")
            user.set_password(user.newPassword)
            user.save()
            raw_password = form.cleaned_data.get("newPassword")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("feed")
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect("login")
    else:
        form = LogInForm()
    return render(request, "login.html", {"form": form})

def about_view(request):
    return render(request, "about.html")
def contact_view(request):
    return render(request, "contact.html")
@login_required
def feed_view(request):
    return render(request, "feed.html")

@login_required
def search_results_view(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        #api call results
        response_data = fetch_articles_from_google_scholar(query, settings.SERP_API_KEY)

        if response_data and 'organic_results' in response_data:
            articles_data = response_data['organic_results']
            #summary_text = generate_summary(articles_data)

            # Kullanıcının arama geçmişini kaydetme işlemi şu anda yapılmayacak
            # Eğer arama geçmişi kaydedilecekse, bu kısım güncellenmelidir
            # if request.user.is_authenticated:
            #     # Burada her bir makale için başlık ve özet bilgilerini birleştirip kaydedebilirsiniz
            #     # Örneğin, paper_titles ve summaries değişkenlerini doldurun ve SearchHistory nesnesi oluşturun

            return render(request, 'search_results.html', {
                'articles_data': articles_data,  # articles yerine articles_data kullanılıyor
                #'summary_text': summary_text,  # Pass summary text
                'user_query': query  # Pass the user query
            })
        else:
            return render(request, 'search_results.html', {
                'error': 'No results found'
            })
    else:
        # POST olmayan istekler için ana sayfaya yönlendir
        return redirect('home')

def save_paper_view(request):
    if request.method == "POST":
        form = FavouritePaperForm(request.POST)
        if form.is_valid():
            favourite_paper = form.save(commit=False)
            favourite_paper.user = request.user
            favourite_paper.save()
            return redirect('favourite_papers')
        else:
            form = FavouritePaperForm()
        return render(request, 'save_paper.html', {'form': form})
