from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/(?P<productName>.+)/$', views.product, name='product_page'),
    url(r'^user/(?P<userName>.+)/$', views.user, name='user_profile')
]
