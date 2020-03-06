from django.conf.urls import url
from basic_app import views

# Template Tagging
# django is gonna look for this app name
app_name = 'basic_app'

urlpatterns = [
    url(r'^other/$', views.other, name = "other"),
    url(r'^relative/$', views.relativeUrl, name = "relativeUrl")
]