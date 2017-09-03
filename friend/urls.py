from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.ADD, name='add'),
    url(r'^new/$', views.NEW, name='new'),
    url(r'^Mylist/$', views.LIST, name='list'),

]

