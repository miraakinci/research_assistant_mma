from ra_app.apis.helper import find_doi, summarize_abstracts, eliminate_duplicates_and_combine, normalise_data
from transformers import BartTokenizer, BartForConditionalGeneration
from ra_app.apis.semanticscholar_api import SemanticScholar
from ra_app.forms import SignUpForm, LogInForm, SearchForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from . models import Article, FavouritePaper
from django.contrib import messages
from django.http import JsonResponse
from ra_app.apis.acm_api import ACM
from ra_app.apis.arxiv_api import Arxiv
from ra_app.apis.sumy_lsa import summarize_lsa
from django.utils.timezone import now
import json

# Create your views here.
def home(request):
    return render(request, "home.html")


def home_or_feed(request):
    if request.user.is_authenticated:
        return redirect("feed")
    else:
        return redirect("home")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.newPassword = form.cleaned_data.get("newPassword")
            user.set_password(user.newPassword)
            user.save()
            raw_password = form.cleaned_data.get("newPassword")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("feed")
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


def feed_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Process the search query
            query = form.cleaned_data.get('query')

            return redirect('search_results', query=query)
        else:
            # Render the feed template w/ form errors
            return render(request, 'feed.html', {'form': form})
    else:
        # Render the feed template w/ empty form
        form = SearchForm()
        return render(request, 'feed.html', {'form': form})


def search_results_view(request):
    model_name_1 = "facebook/bart-large-cnn"
    model_name_2 = "sumy 0.11.0"
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            max_articles = 10
            acm = ACM()
            arxiv = Arxiv()
            sc = SemanticScholar()

            acm_result = acm.acm(query)
            arxiv_result = arxiv.arxiv_query(query, max_results=max_articles)
            sc_result = sc.fetch_papers(query)

            article_titles = []
            for index, row in acm_result.iterrows():
                title = row['Title']
                article_titles.append(title)

            # call habanero library to fetch doi for each article
            doi_list = find_doi(article_titles)
            acm_ss_result = sc.fetch_batch_doi(doi_list)

            normalised_results = normalise_data(
                {
                    'acm': acm_ss_result.to_dict('records'),
                    'arxiv': arxiv_result.to_dict('records'),
                    'sc': sc_result.to_dict('records')
                }
            )

            combined_articles = eliminate_duplicates_and_combine(normalised_results)

            model_name = "facebook/bart-large-cnn"
            tokenizer = BartTokenizer.from_pretrained(model_name)
            model = BartForConditionalGeneration.from_pretrained(model_name)

            combined_summary = []
            for article in combined_articles:
                if article['Abstract'] is not None:
                    summary_text = summarize_lsa(article['Abstract'])

                    #watermark
                    # Generate timestamp
                    timestamp = now().strftime("%Y-%m-%d %H:%M:%S")

                    watermark_info = {
                        'model_name': model_name_2,
                        'timestamp': timestamp,
                        'title': article['Title']
                    }

                    # Publication info as a clickable link
                    publication_link = f"<a href=\"{article['Link']}\" target=\"_blank\">{article['Publication_Info']}</a>"

                    # Combine the summary, watermark, and link into a dictionary
                    combined_summary.append({
                        'summary': f"{summary_text} {publication_link}",
                        'watermark_info': watermark_info
                    })

                    if len(combined_summary) == 3:
                        break

            combined_summary_string = ''.join([i['summary'] for i in combined_summary])
            watermarks_combined = [i['watermark_info'] for i in combined_summary]
            print(watermarks_combined)

            articles_info = []

            #summary here is the abstarct summary
            for article in combined_articles:
                if article['Abstract'] is not None:
                    summary = summarize_abstracts([article['Abstract']], model, tokenizer)[0]
                    timestamp = now().strftime("%Y-%m-%d %H:%M:%S")
                    watermark_info = {
                        'model_name': model_name_1,
                        'timestamp': timestamp,
                        'title': article['Title']
                    }
                    articles_info.append({
                        'title': article['Title'],
                        'summary': summary,
                        'watermark_info': watermark_info,
                        'authors': article['Authors'],
                        'publication_info': article['Publication_Info'],
                        'link': article['Link']
                    })

            return render(request, 'search_results.html', {
                'articles_data': articles_info,
                'user_query': query,
                'combined_summary': combined_summary_string,
                'watermarks_combined': watermarks_combined
            })
        else:
            return render(request, 'feed.html', {'form': form})
    else:
        return redirect('home')


def save_paper_view(request):
    data = json.loads(request.body)
    title = data.get('title')
    link = data.get('link', '')
    authors = data.get('authors', 'Unknown Author')
    publication_info = data.get('publication_info', '')
    abstract = data.get('abstract', '')

    if not title:
        return JsonResponse({'message': 'Title is required'}, status=400)

    article, created = Article.objects.get_or_create(
        title=title,
        defaults={
            'link': link,
            'authors': authors,
            'publication_info': publication_info,
            'abstract': abstract
        }
    )

    FavouritePaper.objects.get_or_create(user=request.user, article=article)
    return JsonResponse({'message': 'Article saved to favourites', 'article_id': article.id}, status=201)


@require_POST
@login_required
def unsave_paper_view(request, paper_id):
    # Get the paper to be unsaved
    paper = FavouritePaper.objects.filter(user=request.user, article_id=paper_id)
    if paper.exists():
        paper.delete()
        return JsonResponse({'message': 'Paper unsaved successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


def display_paper_view(request):
    if request.user.is_authenticated:
        favourite_papers = FavouritePaper.objects.filter(user=request.user).select_related('article')
        context = {'favourite_papers': favourite_papers}
        return render(request, 'library.html', context)


def code_of_conduct_view(request):
    return render(request, 'code_conduct.html')


