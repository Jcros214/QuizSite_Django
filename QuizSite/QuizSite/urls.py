"""QuizSite URL Configuration

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
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


def index(request):
    return render(request, 'home/index.html')


urlpatterns += [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('records/', include('Records.urls')),
    path('quiz/', include('Quiz.urls')),


    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),


#     path('api/', include('api.urls')),

    path('material/', include('Material.urls')),
    path('manager/', include('TournamentManager.urls')),

    # TMP!

    path('rr_gen/', lambda request: render(request, 'RR Generator.html'), name="rr_gen")


]
urlpatterns += staticfiles_urlpatterns()

# from django.contrib.flatpages import views

# urlpatterns += [
#     path('about-us/', views.flatpage, {'url': '/about/'}, name='about'),
#     path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
# ]
