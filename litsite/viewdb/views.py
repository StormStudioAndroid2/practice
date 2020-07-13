from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework_elasticsearch import es_views, es_pagination, es_filters
from .signals import es_client
from django.http import HttpResponse
from .search_indexes import BooksIndex
from six import text_type
from elasticsearch import Elasticsearch, RequestsHttpConnection
import urllib
from elasticsearch_dsl import MultiSearch
# from elasticsearch_dsl import MultiMatch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from .models import Books
from rest_framework import generics
from .search import search
from .serializer import ElasticBooksSerializer
class BooksList(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = ElasticBooksSerializer
    def get_queryset(self):
        q = self.request.query_params.get('q')
        if q is not None:
            return search(q)
        return super().get_queryset()
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def book_view(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    return render(request, 'book_view.html', {'book':book})


class BookPagination(TemplateView):
    template_name = "pagination.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lines = Books.objects.all()
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            page_number = paginator.page(page)
        except EmptyPage:
            page_number = paginator.page(1)
        except PageNotAnInteger:
            page_number = paginator.page(1)
        context['pages'] = page_number
        return context
# class BooksSearchView(es_views.ListElasticAPIView):
#     # es_client = Elasticsearch(hosts=['localhost:9200/'],
#     #                           connection_class=RequestsHttpConnection)
#     # es_model = BooksIndex
#     # es_pagination_class = es_pagination.ElasticLimitOffsetPagination

#     # es_filter_backends = (
#     #     es_filters.ElasticSearchFilter,
#     # )
  
#     # es_search_fields = (
#     #     'title',
#     #     'author'
     
#     # )
#     q = request.GET.get('q', None)
#     page = int(request.GET.get('page', '1'))
#     start = (page-1) * 10
#     end = start + 10

#         query = MultiMatch(query='search', fields=['title', 'author', 'py], fuzziness='AUTO')
#         s = Search(using=elastic_client, index='books').query(query)[start:end]
#         context = super().get_context_data(**kwargs)
#         lines = Books.objects.all()
#         paginator = Paginator(lines, 10)
#         page = self.request.GET.get("page")
#         try:
#             page_number = paginator.page(page)
#         except EmptyPage:
#             page_number = paginator.page(1)
#         except PageNotAnInteger:
#             page_number = paginator.page(1)
#         context['pages'] = page_number
#         return context

class BooksSearchView(TemplateView):
    template_name = "pagination.html"
    # es_client = Elasticsearch(hosts=['localhost:9200/'],
    #                           connection_class=RequestsHttpConnection)
    # es_model = BooksIndex
    # es_pagination_class = es_pagination.ElasticLimitOffsetPagination

    # es_filter_backends = (
    #     es_filters.ElasticSearchFilter,
    # )
  
    # es_search_fields = (
    #     'title',
    #     'author'
    #     'publisher'
    # )
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('search', None)
        page = int(self.request.GET.get('page', '1'))
        start = (page-1) * 10
        end = start + 10
        
        # q = urllib.parse.quote(q.encode('utf8'))
        query = MultiMatch(query=q, fields=['title', 'author', 'publisher'], fuzziness='AUTO')
        s = Search(using=es_client, index='books').query(query)[start:end]
        context = super().get_context_data(**kwargs)
        response = s.execute()
        paginator = Paginator(response, 10)
        page = self.request.GET.get("page")
        try:
            page_number = paginator.page(page)
        except EmptyPage:
            page_number = paginator.page(1)
        except PageNotAnInteger:
            page_number = paginator.page(1)
        context['pages'] = page_number
        return context

