from django.conf.urls import url
from reports import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_report/$', views.get_report, name='get_report'),
]

app_name = 'reports'

