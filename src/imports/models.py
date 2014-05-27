from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django_extensions.db.fields import UUIDField
from model_utils import Choices

from documents.models import Document


@python_2_unicode_compatible
class ImportBatch(models.Model):
    STATUSES = Choices(
        ('new', _('New')),
        ('started', _('Started')),
        ('success', _('Success')),
        ('partial_success', _('Partial success')),
        ('error', _('Error')),
    )

    uid = UUIDField(primary_key=True)
    imported_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Imported document type'),
    )
    file = models.FileField(
        _('File'),
        upload_to='import_%Y%m%d'
    )
    status = models.CharField(
        _('Status'),
        max_length=50,
        choices=STATUSES,
        default=STATUSES.new
    )

    class Meta:
        verbose_name = _('Import batch')
        verbose_name_plural = _('Import batches')

    def __str__(self):
        return 'Import {} ({})'.format(self.uid, self.imported_type)

    def get_absolute_url(self):
        return reverse('import_status', args=[self.uid])


class Import(models.Model):
    batch = models.ForeignKey(
        ImportBatch,
        verbose_name=_('Batch')
    )
    document = models.ForeignKey(
        Document,
        null=True, blank=True
    )
