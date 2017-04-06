from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.storefront, name='store_front'),
    url(r'^storefront/', views.storefront, name='store_front'),
    url(r'^product/(?P<productName>.+)/$', views.product, name='product_page'),
    url(r'^user/(?P<userName>.+)/$', views.user, name='user_profile')
]
