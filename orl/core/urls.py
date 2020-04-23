from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('pre_lancamento/', views.pre_lancamento, name='pre_lancamento'),
    path('lancamento/', views.lancamento, name='lancamento'),
    path('placar_estatico/', views.placar_estatico, name='placar_estatico'),
]
