"""E_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include   
from django.conf import settings
from django.conf.urls import (handler400, handler403, handler404, handler500
)
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
# from allauth.account.url


urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path(_('accounts/'), include('allauth.urls')),

    path("",include("shop.urls",namespace="shop")),
)

# urlpatterns += i18n_patterns(
#     path("",include("shop.urls",namespace="shop")),
# )


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
handler404 = 'shop.views.my_custom_page_not_found_view'
handler500 = 'shop.views.my_custom_error_view'
handler403 = 'shop.views.my_custom_permission_denied_view'
handler400 = 'shop.views.my_custom_bad_request_view'