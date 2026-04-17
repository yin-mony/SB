from django.urls import path

from .user_views import (
    QuickReplyView,
    UserActivityView,
    UserBadgesView,
    UserContentView,
    UserDetailView,
    UserFollowView,
    UserFollowersView,
    UserFollowingView,
    UserHeatmapView,
    UserStatsView,
)

urlpatterns = [
    path("me/quick-reply/", QuickReplyView.as_view()),
    path("<int:user_id>/", UserDetailView.as_view()),
    path("<int:user_id>/stats/", UserStatsView.as_view()),
    path("<int:user_id>/activity/", UserActivityView.as_view()),
    path("<int:user_id>/badges/", UserBadgesView.as_view()),
    path("<int:user_id>/heatmap/", UserHeatmapView.as_view()),
    path("<int:user_id>/follow/", UserFollowView.as_view()),
    path("<int:user_id>/followers/", UserFollowersView.as_view()),
    path("<int:user_id>/following/", UserFollowingView.as_view()),
    path("<int:user_id>/content/", UserContentView.as_view()),
]

