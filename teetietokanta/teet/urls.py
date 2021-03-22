from django.urls import path

from . import views

app_name = 'teet'
urlpatterns = [
    path('', views.index, name='index'),
    path('uusi/', views.addNew, name='addnew'),
    path('lisaa/', views.submitNew, name='submitnew')
]
