import json
from .models import *

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from .documents import *


class NewsDocumentSerializer(DocumentSerializer):
    localites = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta(object):
        model = Ressource
        document = NewsDocument
        fields = (
            'title',
            'content',
            'categories',
            'localites',
        )

    def get_localites(self, obj):
        return [{'nom': loc['nom']} for loc in obj.localites]

    def get_categories(self, obj):
        return [{'nom_categorie': cat['nom_categorie']} for cat in obj.categories]