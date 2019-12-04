from django.conf.urls import url
from . import views
urlpatterns = [url(r'^$', views.dashboard, name='dashboard'), url(r'^instructions$', views.instructions, name='instructions'), url(r'^understood$', views.understood, name='understood'), url(r'^getContent$', views.sendContent, name='sendContent'), url(r'^submitAnnotation$', views.submitAnnotation, name='submitAnnotation'), url(r'^skip$', views.videoSkip, name='videoSkip'), ]
