import datetime

from django.db import transaction
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from accounts.views import LoginRequiredMixin
from documents.utils import get_all_revision_classes
from documents.models import Document
from reviews.models import ReviewMixin, Review


class BatchStartReview(ListView):
    pass


class BaseReviewDocumentList(LoginRequiredMixin, ListView):
    template_name = 'reviews/document_list.html'
    context_object_name = 'revisions'

    def get_context_data(self, **kwargs):
        context = super(BaseReviewDocumentList, self).get_context_data(**kwargs)
        context.update({
            'reviews_active': True,
        })
        return context

    def step_filter(self, qs):
        """Filter document list to get reviews at the current step."""
        raise NotImplementedError('Implement me in the child class.')

    def get_queryset(self):
        """Base queryset to fetch all documents under review.

        Since documents can be of differente types, we need to launch a query
        for every document type that is reviewable.  We assume that the number
        of reviewable document classes will never be too high, so we don't do
        anything to optimize performances for now.

        """
        revisions = []
        klasses = [klass for klass in get_all_revision_classes() if issubclass(klass, ReviewMixin)]

        for klass in klasses:
            qs = klass.objects \
                .exclude(review_start_date=None) \
                .filter(review_end_date=None) \
                .select_related('document')
            qs = self.step_filter(qs)
            revisions += list(qs)

        return revisions


class ReviewersDocumentList(BaseReviewDocumentList):
    """Display the list of documents at the first review step."""

    def get_pending_reviews(self):
        """Get all pending reviews for this user."""
        if not hasattr(self, '_pending_reviews'):
            reviews = Review.objects \
                .filter(reviewer=self.request.user) \
                .filter(reviewed_on=None) \
                .filter(closed=False)

            self._pending_reviews = reviews.values_list('document_id', flat=True)

        return self._pending_reviews

    def step_filter(self, qs):
        pending_reviews = self.get_pending_reviews()

        # A reviewer can only review a revision once
        # Once it's reviewed, the document should disappear from the list
        return qs \
            .filter(reviewers_step_closed=None) \
            .filter(reviewers=self.request.user) \
            .filter(document_id__in=pending_reviews)


class LeaderDocumentList(BaseReviewDocumentList):
    """Display the list of documents at the two first review steps."""

    def step_filter(self, qs):
        return qs \
            .filter(leader_step_closed=None) \
            .filter(leader=self.request.user)


class ApproverDocumentList(BaseReviewDocumentList):
    """Display the list of documents at the third review steps."""

    def step_filter(self, qs):
        return qs.filter(approver=self.request.user)


class ReviewFormView(LoginRequiredMixin, DetailView):
    context_object_name = 'revision'
    template_name = 'reviews/review_form.html'

    def get_context_data(self, **kwargs):
        context = super(ReviewFormView, self).get_context_data(**kwargs)

        user = self.request.user

        can_comment = any((
            (self.object.is_at_review_step('approver') and user == self.object.approver),
            (self.object.is_at_review_step('leader') and user == self.object.leader),
            (self.object.is_at_review_step('reviewers') and self.object.is_reviewer(user))
        ))
        context.update({
            'revision': self.object,
            'reviews': self.object.get_reviews(),
            'is_leader': user == self.object.leader,
            'is_approver': user == self.object.approver,
            'can_comment': can_comment,
        })
        return context

    def check_permission(self, revision, user):
        """Test the user permission to access the current step.

          - A reviewer can only access the review at the fisrt step
          - The leader can access the review at the two first steps
          - The approver can access the review at any step
        """
        if not revision.is_under_review():
            raise Http404()

        # Approver can acces all steps
        elif user == revision.approver:
            pass

        # Leader can only access steps <= approver step
        elif user == revision.leader:
            if revision.leader_step_closed:
                raise Http404()

        # Reviewers can only access the first step
        elif revision.is_reviewer(user):
            if revision.reviewers_step_closed:
                raise Http404()

        # User is not even part of the review
        else:
            raise Http404()

    def get_object(self, queryset=None):
        document_key = self.kwargs.get('document_key')
        qs = Document.objects \
            .filter(category__users=self.request.user)
        document = get_object_or_404(qs, document_key=document_key)
        revision = document.latest_revision

        self.check_permission(revision, self.request.user)

        if revision.is_reviewer(self.request.user) and revision.is_at_review_step('reviewers'):
            qs = Review.objects \
                .filter(document=document) \
                .filter(reviewer=self.request.user) \
                .filter(revision=revision.revision)
            self.review = get_object_or_404(qs)

        return revision

    def get_success_url(self):
        if self.request.user == self.object.approver:
            url = 'approver_review_document_list'
        elif self.request.user == self.object.leader:
            url = 'leader_review_document_list'
        else:
            url = 'reviewers_review_document_list'

        return reverse(url)

    def post(self, request, *args, **kwargs):
        """Process the submitted file and form.

        Multiple cases:
          - A reviewer is submitting a review, submitting a file or not
          - The leader is closing the reviewer step
          - The leader is submitting it's review, with or without file
          - The approver is closing the reviewer step
          - The approver is closing the leader step
          - The approver is submitting it's review, with or without file

        """
        self.object = self.get_object()

        step = self.object.current_review_step()
        step_method = '%s_step_post' % step

        if 'review' in request.POST:
            url = self.get_success_url()
        else:
            url = ''

        # A comment file was submitted
        if hasattr(self, step_method) and 'review' in request.POST:
            getattr(self, step_method)(request, *args, **kwargs)

        # Close XXX step buttons

        if 'close_reviewers_step' in request.POST and request.user in (
                self.object.leader, self.object.approver):
            self.object.end_reviewers_step()

        if 'close_leader_step' in request.POST and request.user == self.object.approver:
            self.object.end_leader_step()

        return HttpResponseRedirect(url)

    @transaction.atomic
    def reviewers_step_post(self, request, *args, **kwargs):
        comments_file = request.FILES.get('comments', None)

        if hasattr(self, 'review'):
            self.review.reviewed_on = datetime.date.today()
            self.review.comments = comments_file
            self.review.closed = True
            self.review.save()

            # If every reviewer has posted comments, close the reviewers step
            qs = Review.objects \
                .filter(document=self.object.document) \
                .filter(revision=self.object.revision) \
                .exclude(reviewed_on=None)
            if qs.count() == self.object.reviewers.count():
                self.object.end_reviewers_step()

    def leader_step_post(self, request, *args, **kwargs):
        comments_file = request.FILES.get('comments', None)

        if self.object.leader == request.user:
            self.object.leader_comments = comments_file
            self.object.end_leader_step(save=False)
            self.object.save()

    def approver_step_post(self, request, *args, **kwargs):
        comments_file = request.FILES.get('comments', None)

        if self.object.approver == request.user:
            self.object.approver_comments = comments_file
            self.object.end_review(save=False)
            self.object.save()
