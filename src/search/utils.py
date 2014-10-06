# -*- coding: utf8 -*-

from __future__ import unicode_literals

from django.db.models.fields import FieldDoesNotExist
from django.db import models

from search import elastic
from django.conf import settings


TYPE_MAPPING = [
    ((models.CharField, models.TextField), 'string'),
    ((models.IntegerField,), 'long'),
    ((models.DecimalField, models.FloatField,), 'double'),
    ((models.DateField, models.TimeField,), 'date'),
    ((models.BooleanField, models.NullBooleanField,), 'boolean'),
]


def get_mapping(doc_class):
    """Creates an elasticsearch mapping for a given document class.

    See: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/mapping.html

    Note: with elasticsearch, sorting cannot be done on "analyzed" values. We
    use multifields so fields can be indexed twice, one analyzed version, and
    one not_analyzed. Thus, we can search, filter, sort or query any field.

    See: http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/multi-fields.html

    """
    revision_class = doc_class.get_revision_class()
    mapping = {
        'properties': {}
    }

    config = doc_class.PhaseConfig
    filter_fields = list(config.filter_fields)
    column_fields = [field[1] for field in config.column_fields]
    fields = filter_fields + column_fields
    for field_name in fields:

        try:
            field = doc_class._meta.get_field_by_name(field_name)[0]
        except FieldDoesNotExist:
            try:
                field = revision_class._meta.get_field_by_name(field_name)[0]
            except FieldDoesNotExist:
                field = None

        es_type = get_mapping_type(field) if field else 'string'

        mapping['properties'].update({
            field_name: {
                'type': es_type,
                'fields': {
                    'raw': {
                        'type': es_type,
                        'index': 'not_analyzed'
                    }
                }
            }
        })

    return mapping


def get_mapping_type(field):
    """Get the elasticsearch mapping type from a django field."""
    for typeinfo, typename in TYPE_MAPPING:
        if isinstance(field, typeinfo):
            return typename
    return 'string'


def index_document(document):
    """Stores a document into the ES index."""
    elastic.index(
        index=settings.ELASTIC_INDEX,
        doc_type=document.document_type(),
        id=document.pk,
        body=document.to_json()
    )


def unindex_document(document):
    """Removes the document from the index."""
    elastic.delete(
        index=settings.ELASTIC_INDEX,
        doc_type=document.document_type(),
        id=document.pk
    )
