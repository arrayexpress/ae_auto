"""ae_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from publications import views as publication_views
from accounts import views as account_views
from logs import views as log_views
# import actstream

# router = routers.DefaultRouter()
# router.register(r'users', views.UserListView)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'publications', publication_views.PublicationList.as_view(), base_name='publication')
# router.register(r'experiments', publication_views.ExperimentList.as_view(), base_name='experiment')
# router.register(r'associations', publication_views.AssociationList.as_view(), base_name='association')
# router.register(r'accounts', account_views.UserListView.as_view(), base_name='a7a')
# router.register(r'logs', log_views.LogListView.as_view(), base_name='log')


from accounts import urls as accounts_urls
from rest_api import urls as rest_api_urls
urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^api/', include(rest_api_urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^publications/$', publication_views.PublicationList.as_view(), name='publication-list'),
    url(r'^publications/(?P<pk>[0-9]+)/$', publication_views.PublicationDetail.as_view(), name='publication-detail'),

)
# urlpatterns = [
#
#     url(r'^', include(router.urls)),
#     url(r'^admin/', include(admin.site.urls)),
#     # url(r'^activity/', include('pinax.eventlog.')),
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#
#     url(r'^publications/$', publication_views.PublicationList.as_view(), name='publication-list'),
#     url(r'^experiments/$', publication_views.ExperimentList.as_view(), name='experiment-list'),
#     url(r'^associations/$', publication_views.AssociationList.as_view(), name='association-list'),
#     # url(r'^logs/$', log_views.LogListView.as_view(), name='log-list'),
#
#
#     url(r'^publications/(?P<pk>[0-9]+)/$', publication_views.PublicationDetail.as_view(), name='publication-detail'),
#     url(r'^experiments/(?P<pk>[0-9]+)/$', publication_views.ExperimentDetail.as_view(), name='experiment-detail'),
#     url(r'^associations/(?P<pk>[0-9]+)/$', publication_views.AssociationDetail.as_view(), name='association-detail'),
#     # url(r'^logs/(?P<pk>[0-9]+)/$', log_views.LogDetail.as_view(), name='log-detail'),
#     # url(r'^activities/(?P<pk>[0-9]+)/$', log_views.LogViewSet, name='log-detail')
#     url(r'^accounts/', include(accounts_urls)),
#     url(r'^api/', include(rest_api_urls)),
#
#
# ]


# urlpatterns = format_suffix_patterns(urlpatterns)
