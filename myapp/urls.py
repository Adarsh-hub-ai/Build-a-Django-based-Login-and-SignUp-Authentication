from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('python/', views.python, name='python'),
    path('login/', views.login, name= 'login'),
    path('signin/', views.signin, name='signin'),
    path('sendcode/', views.sendotp, name='sendotp'),
    path('api/signup/send-code/', views.send_otp, name='send_otp'),
    path('api/signup/verify-code/', views.verify_otp, name='verify_otp'),

]
