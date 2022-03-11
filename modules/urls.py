from . import views
from django.urls import path

app_name = 'modules'
urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.module_json, name='api')
]
