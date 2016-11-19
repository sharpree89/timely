from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.login_home, name='login_home'),
    #redirects to the login page
    url(r'^$', views.register_home, name='register_home'),
    #redirects to the register page
    url(r'^appts$', views.appts, name='appts'),
    #displays today's appts as well as upcoming appts,
    #displays an edit appt link, and a delete appt link
    url(r'^history$', views.history, name='history'),
    #displays user's full appointment history
    url(r'^new$', views.new, name='new'),
    #displays a form to add a new appt
    url(r'^add$', views.add, name='add'),
    # #processes the actual .create() of new appts
    # #redirects to /appts
    url(r'^edit/(?P<appt_id>\d+)$', views.edit, name='edit'),
    # #the edit link redirects to a page w/ a form to edit that appt
    url(r'^process(?P<appt_id>\d+)$', views.process, name='process'),
    # #processes the .save() of editing an existing appt
    # #redirects to /appts
    url(r'^delete/(?P<appt_id>\d+)$', views.delete, name='delete'),
    # #delete link processes the .delete()
    # #redirects to /appts
    url(r'^logout$', views.logout, name='logout')

]
