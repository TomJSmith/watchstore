from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.storefront, name='store_front'),
    url(r'^storefront/', views.storefront, name='store_front'),
    url(r'^choice/(?P<logInSignUp>.+)/$', views.logInSignUpChoice, name='log_in__sign_up_choice'),
    url(r'^signup/(?P<userType>.+)/$', views.signup, name='sign_up'),
    url(r'^login/(?P<userType>.+)/$', views.login, name='log_in'),
    url(r'^product/(?P<productID>.+)/$', views.product, name='product_page'),
    url(r'^merchant/(?P<merchantID>.+)/$', views.merchant, name='merchant_page'),
    url(r'^user/(?P<userName>.+)/$', views.user, name='user_profile'),
    url(r'^search/results/', views.results),
    url(r'^search/', views.search)
]
