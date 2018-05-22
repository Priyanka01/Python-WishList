from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^sucess$', views.sucess),
    
    url(r'^dashboard$',views.dashboard),

    url(r'^additem$', views.additem),
    url(r'^createItem$', views.createItem),
    url(r'^deleteitem/(?P<itemid>\d+)$', views.deleteitem),

    url(r'^addthistomylist/(?P<itemid>\d+)$', views.addthistomylist),
    url(r'^removethisfrommylist/(?P<itemid>\d+)$', views.removethisfrommylist),
    url(r'^itemdetails/(?P<itemid>\d+)$', views.itemdetails),
    
    

    
]