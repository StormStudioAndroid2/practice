from elasticsearch_dsl.query import Q, MultiMatch, SF
from .search_indexes import BooksIndex
from .models import Books

def get_search_query(phrase):
    query = Q(
        'function_score',
        query=MultiMatch(
            fields=['title', 'author', 'publisher'],
            query=phrase
        ),
        functions=[
            SF('field_value_factor', field='number_of_views')
        ]
    )
    return BooksIndex.search().query(query)
def search(phrase):
    return get_search_query(phrase).to_queryset()

