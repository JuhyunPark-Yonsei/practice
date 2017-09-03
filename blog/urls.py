from django.conf.urls import url
from . import views
from .views import MyDetailView
from .models import Post

urlpatterns = [
    url(r'^$', views.post_list, name='index'),
    url(r'^(?P<id>\d+)/$', views.post_detail, name='detail'),
    url(r'^(?P<id>\d+)/$', MyDetailView.as_view(Post), name='detail'),
    url(r'^new/$', views.post_new, name='new'),
    url(r'^(?P<id>\d+)/edit/$', views.post_edit, name='edit'),

]

