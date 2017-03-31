from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^$', views.votes, name='votes'),
    url(r'^wojewodztwo$', views.wojewodztwo, name='wojewodztwo'),
    url(r'^typ$', views.typ, name='typ'),
    url(r'^rozmiar$', views.rozmiar, name='rozmiar'),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),
]