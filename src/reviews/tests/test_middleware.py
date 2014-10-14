# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils import timezone

from categories.factories import CategoryFactory
from documents.factories import DocumentFactory
from accounts.factories import UserFactory
from reviews.models import Review


class ReviewCountMiddleware(TestCase):

    def setUp(self):
        cache.clear()
        self.category = CategoryFactory()
        self.user = UserFactory(
            email='testadmin@phase.fr',
            password='pass',
            is_superuser=True,
            category=self.category
        )
        self.other_user = UserFactory(
            email='test@phase.fr',
            category=self.category
        )
        self.client.login(email=self.user.email, password='pass')
        self.url = reverse('category_list')

    def test_empty_review_list(self):
        res = self.client.get(self.url)

        self.assertContains(res, 'Reviewer (0)')
        self.assertContains(res, 'Leader (0)')
        self.assertContains(res, 'Approver (0)')

    def test_review_step_count(self):
        doc = DocumentFactory(
            revision={
                'reviewers': [self.user, self.other_user],
                'leader': self.user,
                'approver': self.user,
            }
        )
        doc.latest_revision.start_review()
        doc = DocumentFactory(
            revision={
                'reviewers': [self.user, self.other_user],
                'leader': self.other_user,
                'approver': self.user,
            }
        )
        doc.latest_revision.start_review()
        res = self.client.get(self.url)

        self.assertContains(res, 'Reviewer (2)')
        self.assertContains(res, 'Leader (1)')
        self.assertContains(res, 'Approver (2)')

    def test_cancel_review_count(self):
        doc = DocumentFactory(
            revision={
                'reviewers': [self.user, self.other_user],
                'leader': self.user,
                'approver': self.user,
            }
        )
        doc.latest_revision.start_review()
        doc = DocumentFactory(
            revision={
                'reviewers': [self.user, self.other_user],
                'leader': self.other_user,
                'approver': self.user,
            }
        )
        doc.latest_revision.start_review()
        doc.latest_revision.cancel_review()

        res = self.client.get(self.url)

        self.assertContains(res, 'Reviewer (1)')
        self.assertContains(res, 'Leader (1)')
        self.assertContains(res, 'Approver (1)')

    def test_prioritary_review_count(self):
        doc = DocumentFactory(
            revision={
                'reviewers': [self.user],
                'leader': self.user,
                'approver': self.other_user,
                'klass': 1,
            }
        )
        revision = doc.latest_revision
        revision.start_review()
        Review.objects.update(due_date=timezone.now())

        res = self.client.get(self.url)
        self.assertContains(res, 'Priorities (1)')
