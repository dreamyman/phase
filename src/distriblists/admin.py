# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url

from distriblists.models import DistributionList
from distriblists.forms import DistributionListForm
from distriblists.views import DistributionListImport


class DistributionListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('reviewers', 'categories')
    form = DistributionListForm

    def get_urls(self):
        urls = super(DistributionListAdmin, self).get_urls()
        return [
            url(r'^import/$', self.admin_site.admin_view(
                DistributionListImport.as_view(model_admin=self)))
        ] + urls


admin.site.register(DistributionList, DistributionListAdmin)
