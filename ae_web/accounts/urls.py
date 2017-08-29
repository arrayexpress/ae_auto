from django.conf.urls import patterns, url
from .views import LoginView, RegistrationView, LogoutView, EditView

urlpatterns = patterns('',
    url(r'login$', LoginView.as_view()),
    url(r'logout$', LogoutView.as_view()),
    url(r'register$', RegistrationView.as_view()),
    url(r'edit$', EditView.as_view())
)
