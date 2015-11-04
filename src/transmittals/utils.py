# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transmittals import errors
from transmittals.models import TransmittableMixin


class FieldWrapper(object):
    """Utility class to access fields scattered across multiple objects.

    >>> o1 = {'var1': 'toto', 'var2': 'tata'}
    >>> o2 = {'var3': 'riri', 'var4': 'fifi'}
    >>> wrapped = FieldWrapper((o1, o2))
    >>> wrapped.var1
    'toto'
    >>> wrapped.var3
    'riri
    >>> wrapped['var4']
    'fifi'

    """

    def __init__(self, objects):
        self.objects = objects

    def __getitem__(self, attr):
        it = iter(self.objects)

        try:
            obj = it.next()
            while not hasattr(obj, attr):
                obj = it.next()
            return getattr(obj, attr)
        except StopIteration:
            raise AttributeError('Attribute {} not found'.format(attr))

    def __getattr__(self, attr):
        return self[attr]


def create_transmittal(from_category, to_category, revisions):
    """Create an outgoing transmittal with the given revisions."""

    if not isinstance(revisions, list) or len(revisions) == 0:
        raise errors.MissingRevisionsError(
            'Please provide a valid list of transmittals')

    for rev in revisions:
        if not isinstance(rev, TransmittableMixin):
            raise errors.InvalidRevisionsError(
                'At least one of the revisions is invalid.')
