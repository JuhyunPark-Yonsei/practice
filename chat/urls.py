from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.NEW, name='new_room'),
    url(r'^(?P<label>\d+)/$', views.ENTER, name='ENTER'),
    url(r'^roomlist/$', views.LIST, name='LIST'),

]

