from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('python/', views.python, name='python'),
    path('login/', views.login, name= 'login'),
    path('signin/', views.signin, name='signin'),
    path('sendcode/', views.sendotp, name='sendotp')

]
