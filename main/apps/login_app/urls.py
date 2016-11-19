from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login_home, name='login_home'),
    url(r'^signup$', views.register_home, name='register_home'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    # url(r'^success$', views.success, name='success'),
]
