"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from mysite import views

urlpatterns = [
    url(r'^json_data', views.json_data, name='data'),

    url(r'^api/initiatives', views.initiatives, name='initiatives'),
    url(r'^json/initiatives', views.initiatives_json, name='initiatives_json'),
    url(r'^excel/initiatives', views.initiatives_excel, name='initiatives_excel'),

    url(r'^api/contacts', views.contacts, name='contacts'),
    url(r'^json/contacts', views.contacts_json, name='contacts_json'),
    url(r'^excel/contacts', views.contacts_excel, name='contacts_excel'),

    url(r'^api/engagements', views.engagements, name='engagements'),
    url(r'^json/engagements', views.engagements_json, name='engagements_json'),
    url(r'^excel/engagements', views.engagements_excel, name='engagements_excel'),
    
    url(r'^api/community', views.community, name='community'),
    url(r'^json/community', views.community_json, name='community_json'),

    url(r'^api/education', views.education, name='education'),
    url(r'^json/education', views.education_json, name='education_json'),
    url(r'^excel/education', views.education_excel, name='education_excel'),

    url(r'^api/overview', views.overview, name='overview'),
    url(r'^json/overview', views.overview_json, name='overview_json'),
    url(r'^excel/overview', views.overview_excel, name='overview_excel'),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('authentication.urls', namespace="authentication")),

]
