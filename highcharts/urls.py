from django.conf.urls import url
from highcharts import views

handler404 = 'demo.views.custom_404'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^chart_data_json/(?P<csvfile_name>[\w-]+)/$', views.chart_data_json, name='chart_data_json'),
]


