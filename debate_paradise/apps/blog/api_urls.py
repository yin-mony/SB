from django.urls import path

from .api_views import (
    BlogCommentDetailView,
    BlogCoverUploadView,
    BlogNewsletterSubscribeView,
    BlogPostCommentsView,
    BlogPostDetailView,
    BlogPostRelatedView,
    BlogPostsView,
)

urlpatterns = [
    path("covers/upload/", BlogCoverUploadView.as_view()),
    path("subscribe-newsletter/", BlogNewsletterSubscribeView.as_view()),
    path("<int:post_id>/related/", BlogPostRelatedView.as_view()),
    path("<int:post_id>/comments/<int:comment_id>/", BlogCommentDetailView.as_view()),
    path("<int:post_id>/comments/", BlogPostCommentsView.as_view()),
    path("<int:post_id>/", BlogPostDetailView.as_view()),
    path("", BlogPostsView.as_view()),
]
