from xml.dom import minidom
import tempfile
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
import numpy as np
from django.http import HttpResponseRedirect
import cv2
from knox import *
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile

import PIL.Image
from PIL import ImageOps
from PIL import Image  as con
from django.core import serializers
import os
from .form import *
from .serializer import *
# from .haarcascade_frontalface_default.xml import *
from .models import *
import numpy as np
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
# from .serializers import *
from rest_framework import generics, permissions
from django.core.files.base import ContentFile
import yaml
import glob
import threading

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

def loginTest(request):
    global userid
    userid = request.user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        print(request.POST['username'])
        print( request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password was incorrect!')

    return render(request, 'Application/login.html')
def info(request):
    if request.method== "POST":
        return render(request, 'Application/Info.html')
    return render(request, 'Application/Info.html')

def signup(request):
    form = RegisterUser()
    if request.method == "POST":
        form = RegisterUser(request.POST)
        print('-------------------form print-----------------')
        Productid = ProductID.objects.all()
        pid = request.POST['pid']
        
        idexist = False
        ProdExist = False

        ## check if the Product id is exist
        for x in Productid:
            if x.Productid == pid:
                idexist = True
        
        ## check if the product is not register already
        if idexist == True:
            alreadyExist = CustomerProd.objects.all()
            print('------------------------------------')
            print(alreadyExist)
            for exist in alreadyExist:
                temp = str(exist)
                if temp == pid:
                    ProdExist = True
                    messages.info(request, 'One user is already register with this Product Id')

        if ProdExist == True:
            print("one user is already register that product ")
        else:
            print("else")
            if form.is_valid():
                
                # instance.User = request.user
                user = form.cleaned_data.get("username")
                password1 = str(form.cleaned_data.get("password1"))
                password2 = str(form.cleaned_data.get("password2"))
                
                
                
                p = ProductID.objects.get(Productid=request.POST['pid'])
                print('------------------------------------')
                print(p)
                if not p:
                    print("none")
                    messages.info(request, 'Please Check your Product Id number. If you do not have then Purchase isight')
                    context = {'form': form}
                    return render(request, 'Application/signup.html', context)
                
                instance = form.save()
                CustomerProd.objects.create(User=User.objects.get(id=instance.id), customerid=p)
                messages.info(request, 'Sign up successfully! kindly login to Continue')
                return redirect('login')
            else:
                password1 = str(form.cleaned_data.get("password1"))
                password2 = str(form.cleaned_data.get("password2"))
                if (password1 != password2):
                     messages.info(request, 'Incorrect Confirm Password')
                else:
                    messages.info(request, 'This Username Already exist!')
                
    context = {'form': form}
    return render(request, 'Application/signup.html', context)


@login_required(login_url='login')
def home(request):
    allimages = FaceName.objects.filter(User=request.user).count()
    allpdfs = pdf.objects.filter(User=request.user).count()
    context = {
        'allimg':allimages ,
        'allpdfs':allpdfs
    }
    return render(request, 'Application/Deshboard.html' , context)

@login_required(login_url='login')
def pdfs(request):
    if request.method== 'POST':
        book = request.FILES['pdf']
        thumbnail= request.FILES['cover']
        title= request.POST['title']
        desp= request.POST['desp']
        print("------------------------------")
        print(book.name)
        print(book.size) 
        pdf.objects.create(User=User.objects.get(id=request.user.pk) , Pdfstore = book ,title=title,thumbnail=thumbnail,desp=desp )
        
    allPdf =pdf.objects.filter(User=request.user)
    # for p in allPdf:
        # print("http://127.0.0.1:8000/"+p.thumbnail)
    
    context={
        'allPdf' : allPdf
    }    
    return render(request, 'Application/pdf.html',context)

@login_required(login_url='login')
def imagess(request):
    print("redirectttttttttttttt")
    if request.method== 'POST':
        print("redirect from camera")
    else:
        print("in else")
        allimages = FaceName.objects.filter(User=request.user)
        context={
            'allimg' : allimages
        }  
        return render(request, 'Application/imagess.html' , context)

    allimages = Image.objects.filter(User=request.user)
    context={
        'allimg' : allimages
    }  
    return render(request, 'Application/imagess.html' , context)



@login_required(login_url='login')
def pdfDelete(request,id):
    # if request.method== 'POST':
    pdf.objects.get(id=id).delete() 
    allPdf =pdf.objects.filter(User=request.user)
    # for p in allPdf:
        # print("http://127.0.0.1:8000/"+p.thumbnail)
    
    context={
        'allPdf' : allPdf
    }    
    return render(request, 'Application/pdf.html',context)


@login_required(login_url='login')
def imgDelete(request,id):
    # if request.method== 'POST':
    Image.objects.filter(name=id).delete()
    FaceName.objects.filter(name = id).delete()
    allimages = FaceName.objects.filter(User=request.user)
    # for p in allPdf:
        # print("http://127.0.0.1:8000/"+p.thumbnail)
    
    context={
        'allimg' : allimages
    }    
    return render(request, 'Application/imagess.html',context)

def location(request):
    return render(request, 'Application/location.html')

def out(request):
    logout(request)
    return redirect('login')


face_detector = cv2.CascadeClassifier('C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\Application\\haarcascade_frontalface_default.xml')

def face_extractor(img):

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray,1.3,5)

    if faces is None:
        return None
    global cropped_face
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


def hello(request): 
    if request.method == "POST":
        print("check")
        F_name = request.POST['name']
        user_video = request.FILES['vide'] 
        print("checkk")
        print(type(user_video))
        videoSave = videoStore.objects.create(User=User.objects.get(id=request.user.pk) , videoFile = user_video)
        print(videoSave.pk)
        get_path_video = videoStore.objects.get(pk = videoSave.pk)
        print(get_path_video.videoFile)
        accurate_path = "http://127.0.0.1:8000/media/" + str(get_path_video.videoFile)
        print(accurate_path)

        faceCount = FaceName.objects.all().count()
        face_id = faceCount + 1
        count =0
        # print(user_video)
        video = cv2.VideoCapture(accurate_path)
        # Detect object in video stream using Haarcascade Frontal Face
        while True:
                # Capture video frame
            cc, frame = video.read()
            
            if face_extractor(frame) is not None:
                count+=1
                face = cv2.resize(face_extractor(frame),(200,200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                has = cv2.imwrite("static/pdfbook/User." + str(face_id) + '.' + str(count) + ".jpg", face)
                c =  "User." + str(face_id) + '.' + str(count) + ".jpg"
                
                Image.objects.create(User=User.objects.get(id=request.user.pk),  name=F_name , imagestore= c )
            else:
                print("Face not found")
                pass
            if count == 100:
                break  
                
                
    video.release() 
    FaceName.objects.create(User=User.objects.get(id=request.user.pk) , name = F_name , ids = face_id)         
    return redirect('imagess')

def training(request):
    
    # Create Local Binary Patterns Histograms for face recognization
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Using prebuilt frontal face training model, for face detection
    detector = cv2.CascadeClassifier('C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\Application\\haarcascade_frontalface_default.xml')

    getImages = Image.objects.filter(User=request.user)
    faceSamples = []
    ids = []
    count = 0
    for images in getImages:
        count = count + 1
        print("fsdfsdf")
        print(images.imagestore)
        PIL_img = PIL.Image.open(images.imagestore).convert('L')
        # gray_image = ImageOps.grayscale(PIL_img)
            # PIL image to numpy array
        img_numpy = np.array(PIL_img, 'uint8')
        
        
        id = int(os.path.split(str(images.imagestore))[-1].split(".")[1])

            # Get the face from the training images
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
                # Add the image to face samples
            faceSamples.append(img_numpy[y:y + h, x:x + w])
                # Add the ID to IDs
            ids.append(id)

            # Loop for each face, append to their respective ID
        
        
    
    # # Train the model using the faces and IDs
    print(ids)
    print("#############")
    print(faceSamples)
    recognizer.train(faceSamples, np.array(ids))
    
    
    v = "static/pdfbook/" + str(request.user) + "trainer.yml"
    print(v)
    recognizer.save(v)
    print(v)
    d = str(request.user) + "trainer.yml"
    ymlfile.objects.create(User=User.objects.get(id=request.user.pk) , xmlfile= d)
    return redirect('imagess')
################################################### Creating API ###################################################


    

@api_view(['GET'])
@permission_classes((AllowAny,))
def pdfApi(request , pk):
    find_productid = ProductID.objects.get(Productid=pk)
    finduser = CustomerProd.objects.get(customerid=find_productid)
    User = get_user_model()
    users = User.objects.get(username=finduser.User)
    allpdfs = pdf.objects.filter(User=users.pk)
    serializer = PDFSerializer(allpdfs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def xmlfile(request , pk):
    find_productid = ProductID.objects.get(Productid=pk)
    finduser = CustomerProd.objects.get(customerid=find_productid)
    User = get_user_model()
    users = User.objects.get(username=finduser.User)
    xmlfile = ymlfile.objects.filter(User=users.pk)
    serializer = XmlfileSerializer(xmlfile, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def FaceNameApi(request, pk):
    find_productid = ProductID.objects.get(Productid=pk)
    finduser = CustomerProd.objects.get(customerid=find_productid)
    User = get_user_model()
    users = User.objects.get(username=finduser.User)
    findFaceName = FaceName.objects.filter(User=users.pk)
    # print("#################################")
    # print(pk)
    # print(find_productid)
    # print(finduser.User)
    # print("dsd",users.pk)
    # print(findFaceName)
    # print("########################################")
    serializer = FacesSerializer(findFaceName, many=True)
    #data = serializers.serialize('json', findFaceName)
    # return HttpResponse(data, content_type="application/json")
    return Response(serializer.data)

#login API aik sec waitok
@api_view(["POST"])
@csrf_exempt
def loginapi(request):
    permission_classes = (permissions.AllowAny,)
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'user':user.username, 'user_id': user.id,})
    else:
        return Response(" Please Enter correct Username or password") # where is virtual environment
 # signup API

@api_view(["POST"])
@permission_classes((AllowAny,))
def signupapi(request):
    username = request.data.get('username')
    password = request.data.get("password")
    p_id = request.data.get("id")
    
    Productid = ProductID.objects.all()
    idexist = False
    ProdExist = False

     ## check if the Product id is exist
    for x in Productid:
        if x.Productid == p_id:
            idexist = True
        
        ## check if the product is not register already
    if idexist == True:
        alreadyExist = CustomerProd.objects.all()
        print('------------------------------------')
        print(alreadyExist)
        for exist in alreadyExist:
            temp = str(exist)
            if temp == p_id:
                ProdExist = True
                return Response({"msg":"One User is Already Register with this Product Id"})

    if ProdExist == True:
        print("one user is already register that product ")
    else:
        p = ProductID.objects.get(Productid=p_id)
        if not p:
            print("none")
            return Response({"msg":"Product Id is incorrect"})
        user_obj = User(username=username)
        user_obj.set_password(password)
        instance =user_obj.save()
        c = User.objects.get(username=user_obj)
        pid = ProductID.objects.get(Productid=p_id)
        CustomerProd.objects.create(User=User.objects.get(id=c.id), customerid=pid)
        return Response({"msg": "created successfully"},status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def pdfApiMobile(request , pk):
    allpdfs = pdf.objects.filter(User=User.objects.get(id=pk))
    serializer = PDFSerializer(allpdfs, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def pdfdelete(request , pk):
    allpdfs = pdf.objects.get(id=pk).delete()
    return Response("deleted successfully")


@api_view(['POST'])
@permission_classes((AllowAny,))
def addpdfmobile(request):
    pdfobj = pdf.objects.create(
        User=User.objects.get(id=request.data['id']),
        title=request.data['title'],
        desp=request.data['desp'],
        Pdfstore=request.FILES['pdfstore'],
        thumbnail = request.FILES['thumbnail'],
        )
    allpdfs = pdf.objects.filter(User=User.objects.get(id=request.data['id']))
    serializer = PDFSerializer(allpdfs, many=True)
    return Response(serializer.data)


class logintest(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
       
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data['user']
            login(request, user)
            return Response({"user": UserSerializer(user).data,})
        else:
            return Response({
                "user":"Invalid Creditential"
            })
        
        