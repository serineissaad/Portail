from django_elasticsearch_dsl import Document, fields, Index
from .models import Ressource, Categorie, Localite
from elasticsearch_dsl import analyzer

# Define the custom analyzer using the asciifolding filter
folding_analyzer = analyzer(
    'myanalyzer',
    tokenizer='standard',
    filter=['lowercase', 'asciifolding']
)

# Define the Elasticsearch index for Ressource documents
PUBLISHER_INDEX = Index('ressource_demo')
PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1,
    analysis={
        'analyzer': {
            'myanalyzer': folding_analyzer.get_analysis_definition()
        }
    }
)

@PUBLISHER_INDEX.document
class NewsDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        attr='titre',
        analyzer=folding_analyzer #'myanalyzer'
    )
    content = fields.TextField(
        attr='description', 
        analyzer=folding_analyzer #'myanalyzer'
    )

    # Adjusted fields for ManyToMany relationships
    categories = fields.NestedField(properties={
        'nom_categorie': fields.TextField(
            analyzer=folding_analyzer#'myanalyzer'
            ),
    })

    localites = fields.NestedField(properties={
        'nom': fields.TextField(
            analyzer=folding_analyzer#'myanalyzer'
            ),
    })

    class Index:
        name = 'ressource_demo'

    class Django:
        model = Ressource  # Specifies the Django model
        related_models = [Categorie, Localite]  # Related models that trigger reindexing

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, (Categorie, Localite)):
            return related_instance.ressources.all()