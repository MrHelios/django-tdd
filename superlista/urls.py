from django.conf.urls import url
from lista import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
]
