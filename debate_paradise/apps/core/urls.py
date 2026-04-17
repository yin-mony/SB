from django.urls import include, path

from .views import FavoritesStatusView, FavoritesView, HealthView, NotificationReadView, NotificationsReadAllView, NotificationsView

urlpatterns = [
    path("health/", HealthView.as_view()),
    path("auth/", include("apps.users.urls")),
    path("users/", include("apps.users.user_urls")),
    path("topics/", include("apps.debate.api_urls")),
    path("blog-posts/", include("apps.blog.api_urls")),
    path("favorites/", FavoritesView.as_view()),
    path("favorites/status/", FavoritesStatusView.as_view()),
    path("notifications/", NotificationsView.as_view()),
    path("notifications/<int:notification_id>/read/", NotificationReadView.as_view()),
    path("notifications/read-all/", NotificationsReadAllView.as_view()),
]
