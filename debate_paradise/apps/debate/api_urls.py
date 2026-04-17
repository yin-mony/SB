from django.urls import path

from .api_views import (
    DebatePostDetailView,
    TopicCategoriesView,
    TopicDetailView,
    TopicPostsView,
    TopicsView,
    TopicVoteView,
)

urlpatterns = [
    path("categories/", TopicCategoriesView.as_view()),
    path("", TopicsView.as_view()),
    path("<int:topic_id>/", TopicDetailView.as_view()),
    path("<int:topic_id>/posts/<int:post_id>/", DebatePostDetailView.as_view()),
    path("<int:topic_id>/posts/", TopicPostsView.as_view()),
    path("<int:topic_id>/vote/", TopicVoteView.as_view()),
]

