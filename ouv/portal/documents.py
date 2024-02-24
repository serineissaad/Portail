from django_elasticsearch_dsl import Document, fields, Index
from .models import Ressource, Categorie, Localite

# Assuming the Index and settings are correctly defined as before
PUBLISHER_INDEX = Index('ressource_demo')
PUBLISHER_INDEX.settings(number_of_shards=1, number_of_replicas=1)

@PUBLISHER_INDEX.document
class NewsDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        attr='titre',
        # fields={
        #     'raw': {
        #         'type': 'keyword',
        #     }
        # }
    )
    content = fields.TextField(
        attr='description',
        # fields={
        #     'raw': {
        #         'type': 'keyword',
        #     }
        # },
    )

    # Adjusted fields for ManyToMany relationships
    categories = fields.NestedField(properties={
        'nom_categorie': fields.TextField(),
    })

    localites = fields.NestedField(properties={
        'nom hihi': fields.TextField(),
    })

    class Django:
        model = Ressource
        related_models = [Categorie, Localite]

    def get_instances_from_related(self, related_instance):
        """Handle reindexing of Ressource documents when related instances change."""
        if isinstance(related_instance, (Categorie, Localite)):
            return related_instance.ressource_set.all()
