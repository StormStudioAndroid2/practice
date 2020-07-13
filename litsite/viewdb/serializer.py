from __future__ import (absolute_import, division, print_function, unicode_literals)
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer

from .models import Books
from .search_indexes import BooksIndex


class ElasticBooksSerializer(ElasticModelSerializer):
    class Meta:
        model = Books
        es_model = BooksIndex
        fields = ('title', 'author', 'publisher')
