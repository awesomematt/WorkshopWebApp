from django.conf.urls import url

from . import views

app_name = 'orders'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mybox/$', views.shoppingBox, name='mybox'),
    url(r'^finalize/$', views.finalize, name='finalize'),
    url(r'^summary/$', views.order_info, name='summary'),
]
