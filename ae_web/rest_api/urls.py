from maintenance.views import RestartFramework, validate_data_files_view
from publications.views import EditPublication

__author__ = 'Ahmed G. Ali'
from django.conf.urls import patterns, url
from accounts import views as accounts_views
from publications import views as publications_views
urlpatterns = patterns(
    '',
    url(r'^me/?$', accounts_views.MeView.as_view()),
    url(r'^users/?$', accounts_views.UserListView.as_view()),
    url(r'^users/(?P<pk>\d+)/?$',
        accounts_views.UserDetailView.as_view()),
    # url(r'^publications/?$', publications_views.PublicationList.as_view()),
    # url(r'^publications/(?P<pk>\d+)/$',
    #     publications_views.PublicationDetail.as_view()),
    # url(r'^publications/(?P<pk>[0-9]+)/$', publications_views.PublicationDetail.as_view(), name='publication-detail')
    url(r'^publications/?$', publications_views.AssociationList.as_view()),
    url(r'^publications/(?P<pk>[0-9]+)/$', publications_views.AssociationDetail.as_view(), name='association-detail'),
    url(r'^publications/edit$', EditPublication.as_view()),
    url(r'^maintenance/framework/restart$', RestartFramework.as_view()),
    url(r'^validate/(?P<job_id>[\w\-]+)/$', validate_data_files_view),
    url(r'^validate/$', validate_data_files_view)
    # url(r'^validate/?$', validate_data_files_view)
)