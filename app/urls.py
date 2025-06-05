from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from app.core import views as core_views
from app.swagger import schema_view

# from app.schedules import views as schedules_views
# from app.workouts import views as workouts_views

# Overriding AdminSite attributes.
admin.site.site_header = admin.site.site_title = "back-end-biceps"

# API URLs.
router = routers.SimpleRouter()
router.register("users", core_views.UserViewSet, basename="user")
router.register("students", core_views.StudentViewSet, basename="student")
# router.register('schedules', schedules_views.SchedulesViewSet, basename='schedules')
# router.register('workouts', workouts_views.WorkoutsViewSet, basename='workouts')

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin URLs
    path("api/", include(router.urls)),  # API URLs
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT token obtain URL
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # JWT token refresh URL
    path(
        "api/token/verify/", TokenVerifyView.as_view(), name="token_verify"
    ),  # JWT token verify URL
]

# Include specific URLs, only on debug mode.
if settings.DEBUG:
    urlpatterns += [
        path("api/auth/", include("rest_framework.urls")),  # REST framework auth URLs
        path(
            "api/swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"
        ),  # Swagger UI
        path(
            "api/redoc/", schema_view.with_ui("redoc"), name="schema-redoc"
        ),  # ReDoc UI
    ]
    urlpatterns += debug_toolbar_urls()  # Debug toolbar URLs

# Include static URLs.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
