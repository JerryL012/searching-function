from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# BASE_URL = 'http://university.bath.org/search/?query={}'
BASE_URL = 'https://losangeles.craigslist.org/search/?query={}'

# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    # get the POST request from the "base.html, name='search'", POST is a dictionary.
    search = request.POST.get('search')
    # put it in database
    models.Search.objects.create(search=search)

    # turn it into http://university.bath.org/search/?query=hello+i+am+here
    final_url = BASE_URL.format(quote_plus(search))
    # get the HTML data in final_url
    responese = requests.get(final_url)
    data = responese.text
    # parse the data into Beautifulsoup object
    soup = BeautifulSoup(data, features='html.parser')
    # find all the li whose class is result-row
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # loop through it
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_= 'result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,

    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
