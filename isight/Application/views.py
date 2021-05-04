from xml.dom import minidom

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import numpy as np
import cv2
import PIL.Image
from django.core import serializers
import os
from .form import *
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


def signup(request):
    form = RegisterUser()
    if request.method == "POST":
        form = RegisterUser(request.POST)
        print('-------------------form print-----------------')
        print(form)
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
            if form.is_valid():
                instance = form.save()
                # print(instance.pk)
                print('------------------------------------')
                ##instance.User = request.user
                user = form.cleaned_data.get("username")
                # print(instance.id)
                
                p = ProductID.objects.get(Productid=request.POST['pid'])
                print('------------------------------------')
                print("asd" ,p)
                CustomerProd.objects.create(User=User.objects.get(id=instance.id), customerid=p)
                return redirect('login')
            else:
                messages.info(request, 'This Username Already exist!')
                print("user already exit ")
    context = {'form': form}
    return render(request, 'Application/signup.html', context)


@login_required(login_url='login')
def home(request):
    allimages = Image.objects.filter(User=request.user).count()
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
    if request.method== 'POST':
        img = request.FILES['imgs']
        nameu = request.POST['name']
        
        Image.objects.create(User=User.objects.get(id=request.user.pk) , imagestore = img , name = nameu)
    
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
    Image.objects.get(id=id).delete()
    allimages = Image.objects.filter(User=request.user)
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


# Import OpenCV2 for image processing

def hello(request):
    print('asim')
    acd=FaceName.objects.all().count()

    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
    print('raza')
    # Start capturing video
    vid_cam = cv2.VideoCapture(0)
    # xmldoc = minidom.parse('haarcascade_frontalface_default.xml')
    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\Application\\haarcascade_frontalface_default.xml')


    # For each person, one face id
    face_id = acd+1

    # Initialize sample face image
    count = 0

    assure_path_exists("dataset/")

    # Start looping
    while(True):

        # Capture video frame
        _, image_frame = vid_cam.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x,y,w,h) in faces:

            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)

            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            has = cv2.imwrite("static/pdfbook/images/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            print("has" , has)
            c = 'C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\static\\pdfbook\\images\\' + "User." + str(face_id) + '.' + str(count) + ".jpg"
            im = cv2.imread(c)

            #############################dataset/


            nameu = "unknown"
            Image.objects.create(User=userid, imagestore= c, name=nameu)


            #############################
            face = cv2.resize(image_frame, (400, 400))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', face)

        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        # If image taken reach 100, stop taking video
        elif count>100:
            break

    # Stop video
    vid_cam.release()

    # Close all started windows
    cv2.destroyAllWindows()
    res=FaceName.objects.create(name=request.POST['name'],ids=face_id)
    print(res)

    return redirect('imagess')

def training(request):
    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    # Create Local Binary Patterns Histograms for face recognization
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Using prebuilt frontal face training model, for face detection
    detector = cv2.CascadeClassifier('C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\Application\\haarcascade_frontalface_default.xml');

    # Create method to get the images and label data
    def getImagesAndLabels(path):

        # Get all file path
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        # Initialize empty face sample
        faceSamples = []

        # Initialize empty id
        ids = []

        # Loop all the file path
        for imagePath in imagePaths:

            # Get the image and convert it to grayscale

            PIL_img = PIL.Image.open(imagePath).convert('L')

            # PIL image to numpy array
            img_numpy = np.array(PIL_img, 'uint8')

            # Get the image id
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            # Get the face from the training images
            faces = detector.detectMultiScale(img_numpy)

            # Loop for each face, append to their respective ID
            for (x, y, w, h) in faces:
                # Add the image to face samples
                faceSamples.append(img_numpy[y:y + h, x:x + w])

                # Add the ID to IDs
                ids.append(id)

        # Pass the face array and IDs array
        return faceSamples, ids

    # Get the faces and IDs
    faces, ids = getImagesAndLabels('C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\static\\pdfbook\\images\\')
    print(faces)

    # Train the model using the faces and IDs
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer.yml
    assure_path_exists('trainer/')
    recognizer.save('trainer/trainer.yml')
    return redirect('imagess')


################################################### Creating API ###################################################

@api_view(['GET'])
@permission_classes((AllowAny,))
def xmlApi(request):
    # if request.method == 'GET':

    # abc=
    with open("C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\trainer\\trainer.yml", 'r') as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    files = glob.glob('C:\\Users\\abbas\\Desktop\\final try\\FYP\\isight\\trainer\\trainer.yml')
    # print(files)
    # one_h_ago = timezone.now() - timezone.timedelta(hours=1)

    # queryset = Post.objects.filter(date_time__gte=one_h_ago)
    context={
        'abc':files
    }
    # serializer_class = lasthourpostsSerializer(queryset, many=True)
    return Response(files)


@api_view(['GET'])
@permission_classes((AllowAny,))
def pdfApi(request):
    allpdfs=pdf.objects.filter(User=request.user)
    data = serializers.serialize('json', allpdfs)
    # return HttpResponse(data, content_type="application/json")
    return Response(data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def FaceNameApi(request):
    allFaceName = FaceName.objects.all()
    data = serializers.serialize('json', allFaceName)
    # return HttpResponse(data, content_type="application/json")
    return Response(data)