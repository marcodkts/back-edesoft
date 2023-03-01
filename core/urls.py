"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.tools.openapi import LoginSpectacularAPIView, LoginSpectacularRedocView, LoginSpectacularSwaggerView
from back_edesoft import urls as back_edesoft_urls

urlpatterns = [
    path("api/", include(back_edesoft_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.SHOW_DJANGO_PAGES:
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("__debug__/", include(debug_toolbar.urls)),
        path(
            "swagger/",
            LoginSpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("redoc/", LoginSpectacularRedocView.as_view(url_name="schema"), name="redoc"),
        path("__schema__/", LoginSpectacularAPIView.as_view(), name="schema"),
    ]
