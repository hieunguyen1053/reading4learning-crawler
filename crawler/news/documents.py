from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import News


@registry.register_document
class NewsDocument(Document):
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
