from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Category, News


@registry.register_document
class NewsDocument(Document):
    categories = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    class Index:
        name = 'news'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = News
        fields = [
            'uuid',
            'title',
            'html_content',
            'content',
            'author',
            'date_published',
            'lead_image_url',
            'url',
            'domain',
            'word_count',
            'statistics',
            'created_at',
            'updated_at',
        ]
        related_models = [Category,]

    def get_instances_from_related(self, related_instance):
        return related_instance.news_set.all()

    def prepare_categories(self, instance):
        return [
            {
                'uuid': category.uuid,
                'name': category.name,
            }
            for category in instance.categories.all()
        ]
