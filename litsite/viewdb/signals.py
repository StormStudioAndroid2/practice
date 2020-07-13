from __future__ import (absolute_import, division, print_function, unicode_literals)

from elasticsearch import Elasticsearch, RequestsHttpConnection

es_client = Elasticsearch(
    hosts=['localhost:9200/'],
    connection_class=RequestsHttpConnection
)
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .serializer import Books, ElasticBooksSerializer


@receiver(pre_save, sender=Books, dispatch_uid="update_record")
def update_es_record(sender, instance, **kwargs):
    obj = ElasticBooksSerializer(instance)
    obj.save(using=es_client)


@receiver(post_delete, sender=Books, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = ElasticBooksSerializer(instance)
    obj.delete(using=es_client, ignore=404)
    