from django.urls import path

from . import views

app_name = 'blackhatbase'
urlpatterns = [
    path('', views.index, name='index'),
    path('sendcontent/', views.submitNew, name='sendcontent')
]
