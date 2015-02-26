'''
Created on Oct 5, 2014

@author: santhosh
'''
from django.conf.urls import patterns, url
from registration import views




urlpatterns=patterns('',
                    # url(r'^$',views.register,name='register'),
                      url(r'^$',views.index,name='index'),
                      url(r'^bigdata$',views.bigdata,name='bigdata'),
                     url(r'^submitDetails/$',views.processData,name='processData'),)
#urlpatterns += staticfiles_urlpatterns()