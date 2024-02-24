# from django.shortcuts import render
# from django.http import JsonResponse
# import requests
# import json
# from .models import *
# from .documents import *
from .serializers import *

# from django.shortcuts import render
# from .documents import NewsDocument  # Ensure correct import path

# def index(request):
#     search_query = request.GET.get('search', '')
#     if search_query:
#         # Perform search using Elasticsearch
#         # search_results = NewsDocument.search().query("multi_match", query=search_query, fields=['title', 'content','categorie','localite']).to_queryset()
#         search_results = NewsDocument.search().query("multi_match", query=search_query, fields=['title', 'content', 'categories.nom_categorie', 'localites.nom']).to_queryset()
#     else:
#         search_results = []

#     return render(request, 'index.html', {'resources': search_results})



from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)

    
# def generate_random_data():
#     url = 'https://newsapi.org/v2/everything?q=apple&from=2021-04-23&to=2021-04-23&sortBy=popularity&apiKey=f50ebeca2fa344f9be71abde5108831e'
    
#     r = requests.get(url)
#     payload = json.loads(r.text)
    
#     print("Status Code:", r.status_code)
#     print("Response description:", r.text[:500])  # Print the first 500 characters of the response

#     articles = payload.get('articles', [])  # Use an empty list if 'articles' key is not found
#     count = 1
#     for data in articles:  # This will not raise an error if 'articles' is missing
#         print(count)
#         Ressource.objects.create( 
#             title=data.get('title'),
#             content=data.get('content'),
#             categories=data.get('categories'),
#             localites=data.get('localites'),
#             ##heeeeere could add categorie to display
#         )
#         count += 1

from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from .models import Ressource
from .documents import NewsDocument
from elasticsearch_dsl import Q

def index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        query = Q("nested", 
                  path="categories",
                  query=Q("match", categories__nom_categorie=search_query)) | \
                Q("nested", 
                  path="localites",
                  query=Q("match", localites__nom=search_query)) | \
                Q("multi_match", query=search_query, fields=['title', 'content']) 
                  
        search_results = NewsDocument.search().query(query).to_queryset()
        print("here results: " ,search_results)
    else:
        search_results = []
        print('riiiiiieeeeen')

    return render(request, 'index.html', {'resources': search_results})

def generate_random_data():
    url = 'https://newsapi.org/v2/everything?q=apple&from=2021-04-23&to=2021-04-23&sortBy=popularity&apiKey=YOUR_API_KEY'
    
    r = requests.get(url)
    payload = json.loads(r.text)
    
    print("Status Code:", r.status_code)
    print("Response description:", r.text[:500])  # Print the first 500 characters of the response

    articles = payload.get('articles', [])  # Use an empty list if 'articles' key is not found
    count = 1
    for data in articles:  # This will not raise an error if 'articles' is missing
        # print(count)
        # # Note: The following line needs adjustment to correctly handle ManyToMany relationships
        # # You'll need to create categories and localites instances and add them to the Ressource
        ressource = Ressource.objects.create(
            titre=data.get('title'),
            description=data.get('content')
        )
        # Add logic here to associate categories and localites with the ressource
        count += 1



class PublisherDocumentView(DocumentViewSet):
    document = NewsDocument
    serializer_class = NewsDocumentSerializer
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
   
    search_fields = (
        'title',
        'content',
        'categories',
        'localites',
    )
    multi_match_search_fields = (
        'title',
        'content',
        'categories',
        'localites',
    )
    filter_fields = {
        'title': 'title',
        'content': 'content',
        'categories': 'categories',
        'localites': 'localites' ,
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ('id',)