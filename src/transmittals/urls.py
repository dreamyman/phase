# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from transmittals.views import (
    TransmittalListView, TransmittalDiffView, TransmittalRevisionDiffView,
    DemoDiffView, DemoRevisionDiffView)

urlpatterns = patterns(
    '',
    url(r'^$',
        TransmittalListView.as_view(),
        name="transmittal_list"),
    url(r'^(?P<transmittal_pk>\d+)/(?P<transmittal_key>[\w-]+)/$',
        TransmittalDiffView.as_view(),
        name='transmittal_diff'),
    url(r'^(?P<transmittal_pk>\d+)/(?P<transmittal_key>[\w-]+)/(?P<document_key>[\w-]+)/(?P<revision>\d+)/$',
        TransmittalRevisionDiffView.as_view(),
        name='transmittal_revision_diff'),


    # Demo views
    url(r'^transmittal/$',
        DemoDiffView.as_view(),
        name="demo_transmittal_diff_view"),
    url(r'^revision/$',
        DemoRevisionDiffView.as_view(),
        name="demo_revision_diff_view"),
)
