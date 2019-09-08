"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from todos.views import tempo_atual
from todos.views import SobreView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers
from todos import viewsets
from snippets.viewsets import UserViewSet, SnippetViewSet

router = routers.DefaultRouter()
# router.register(r'users', viewsets.UserViewSet)
router.register(r'users', UserViewSet)
router.register(r'snippets', SnippetViewSet)
router.register(r'groups', viewsets.GroupViewSet)

urlpatterns = [
    #path('', include('snippets.urls')),
    path('admin/', admin.site.urls),
    path('todos/', include('todos.urls')),
    path('sobre/', SobreView.as_view()),
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
