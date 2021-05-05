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

  
    path('pdfApi/<str:pk>/', views.pdfApi, name='pdfApi'),
    path('FaceNameApi/<str:pk>/', views.FaceNameApi, name='FaceNameApi'),
    path('xmlfile/<str:pk>/', views.xmlfile, name='xmlfile'),

]