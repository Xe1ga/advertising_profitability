from django.conf.urls import url
from reports import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]

app_name = 'reports'

