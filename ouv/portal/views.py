from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from .models import *
from .documents import *
from .serializers import *

# def index (request):
#     return render(request,'index.html')

from django.shortcuts import render
from .documents import NewsDocument  # Ensure correct import path

def index(request):
    search_query = request.GET.get('search', '')
    if search_query:
        # Perform search using Elasticsearch
        search_results = NewsDocument.search().query("multi_match", query=search_query, fields=['title', 'content']).to_queryset()
    else:
        search_results = []

    return render(request, 'index.html', {'resources': search_results})



from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)

    
def generate_random_data():
    url = 'https://newsapi.org/v2/everything?q=apple&from=2021-04-23&to=2021-04-23&sortBy=popularity&apiKey=f50ebeca2fa344f9be71abde5108831e'
    
    r = requests.get(url)
    payload = json.loads(r.text)
    
    print("Status Code:", r.status_code)
    print("Response description:", r.text[:500])  # Print the first 500 characters of the response

    articles = payload.get('articles', [])  # Use an empty list if 'articles' key is not found
    count = 1
    for data in articles:  # This will not raise an error if 'articles' is missing
        print(count)
        Ressource.objects.create( 
            title=data.get('title'),
            content=data.get('content')
        )
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
    )
    multi_match_search_fields = (
        'title',
        'content',
    )
    filter_fields = {
        'title': 'title',
        'content': 'content',
    }
    ordering_fields = {
        'id': None,
    }
    ordering = ('id',)



