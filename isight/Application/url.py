from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginTest, name='login'),
    path('signup', views.signup , name='signup'),
    path('home', views.home , name='home'),
    path('pdf', views.pdfs , name='pdf'),
    path('imagess', views.imagess , name='imagess'),
    path('pdfDelete/<int:id>', views.pdfDelete , name='pdfDelete'),
    path('imgDelete/<int:id>', views.imgDelete , name='imgDelete'),
    path('location', views.location , name='location'),
    path('out', views.out , name='out'),
    path('hello', views.hello, name='hello'),
    path('training', views.training, name='training'),

    path('xmlApi', views.xmlApi, name='xmlApi'),
    path('pdfApi', views.pdfApi, name='pdfApi'),
    path('FaceNameApi', views.FaceNameApi, name='FaceNameApi'),

]