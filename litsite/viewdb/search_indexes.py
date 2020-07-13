from __future__ import (absolute_import, division, print_function, unicode_literals)
from .models import Books

from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import  Date, Integer, Keyword, Text, GeoPoint, DocType
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])
es_client = Elasticsearch(
    hosts=['localhost:9200/'],
    connection_class=RequestsHttpConnection
)
class BooksIndex(DocType):
    publisher = Text()
    author = Text(analyzer='snowball', fields={'raw': Keyword()})
    title = Text(analyzer='snowball')
    class Meta:
        index = 'books'


BooksIndex.init()


books = Books.objects.all()
i = 0
for book in books:
    i+=1
    book_new_index = BooksIndex(meta={'id': i})
    book_new_index.title = book.title
    book_new_index.author = book.author
    book_new_index.publisher = book.publisher
    book_new_index.save()


