from django.conf.urls import url
from . import views
urlpatterns = [url(r'^login$', views.loginUser, name='loginUser'),
               url(r'^login.html$', views.loginPage, name='loginPage'),
               url(r'^navbar.html$', views.navbar, name='navbar'),
               url(r'^signup.html$', views.signupPage, name='signupPage'),
               url(r'^$', views.homepage, name='homepage'),
               url(r'^register$', views.registerUser, name='registerUser'),
               url(r'^verifyOTP$', views.verifyOtp, name='verifyOtp'),
               url(r'^logout$',views.logout, name='logout')
               ]
