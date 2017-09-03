from django.conf.urls import url
from . import views
from . import views_cbv

urlpatterns = [
    url(r'^$', views.post_list, name='index'),

    url(r'^list1/$', views.post_list1),
    url(r'^list2/$', views.post_list2),
    url(r'^list3/$', views.post_list3),
    url(r'^excel/$', views.excel_download),

    url(r'^cbv/list1/$', views_cbv.PostListView1.as_view()),
    url(r'^cbv/list2/$', views_cbv.PostListView2.as_view()),
    url(r'^cbv/list3/$', views_cbv.PostListView3.as_view()),
    url(r'^cbv/excel/$', views_cbv.ExcelDownloadView.as_view()),

    url(r'^new/$', views.post_new),
    url(r'^(?P<id>\d+)/edit/$', views.post_edit),

]
