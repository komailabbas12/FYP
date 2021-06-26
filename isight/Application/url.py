from django.urls import path
from . import views
from knox import views as knox_views
from .views import logintest

urlpatterns = [
    path('', views.info, name='Info'),
    path('login', views.loginTest, name='login'),
    path('signup', views.signup , name='signup'),
    path('deshboard', views.home , name='home'),
    path('send-book', views.pdfs , name='pdf'),
    path('Person-identification', views.imagess , name='imagess'),
   
    path('book-delete/<int:id>', views.pdfDelete , name='pdfDelete'),
    path('person-identity-delete/<str:id>', views.imgDelete , name='imgDelete'),
    path('location', views.location , name='location'),
    path('out', views.out , name='out'),
    path('hello', views.hello, name='hello'),
    path('training', views.training, name='training'),
    path('login-api/', views.loginapi, name='login-api'),
    path('signupapi/', views.signupapi, name='signupapi'),
    # path('pdfbyUserAPI/<int:pk>/', views.PdfbyUserAPI, name=
    #      'productsByCategoryAPI'),



  
    path('pdfApi/<str:pk>/', views.pdfApi, name='pdfApi'),
    path('addpdfmobile/', views.addpdfmobile, name='addpdfmobile'),
    path('pdfdelete/<str:pk>/', views.pdfdelete, name='pdfdelete'),
    path('pdfApiMobile/<str:pk>/', views.pdfApiMobile, name='pdfApiMobile'),
    path('FaceNameApi/<str:pk>/', views.FaceNameApi, name='FaceNameApi'),
    path('xmlfile/<str:pk>/', views.xmlfile, name='xmlfile'),

    path('logintest/', logintest.as_view(), name='logintest'),

]