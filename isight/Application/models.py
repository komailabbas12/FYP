from django.db import models
from django.contrib.auth.models import User



class ProductID(models.Model):
    Productid = models.CharField(max_length=200)
    def __str__(self):
        return self.Productid
    

class CustomerProd(models.Model):
    User = models.OneToOneField(User, null=True, on_delete= models.SET_NULL , )
    customerid = models.OneToOneField('ProductID', null=True, on_delete= models.SET_NULL  )
    
    def __str__(self):
        return str(self.customerid)


class pdf(models.Model):
    User = models.ForeignKey(User, null=True ,  on_delete= models.SET_NULL)
    Pdfstore = models.FileField(null=True)
    thumbnail = models.FileField(null=True,blank=True)
    title = models.CharField(max_length=200)
    desp = models.CharField(max_length=200)
    def __str__(self):
        return str(self.title)


class Image(models.Model):
    User = models.ForeignKey(User, null=True ,  on_delete= models.SET_NULL)
    name = models.CharField(max_length=200, null=True,blank=True)
    imagestore = models.FileField(null=True)
    def __str__(self):
        return str(self.name)

class FaceName(models.Model):
    User = models.ForeignKey(User, null=True ,  on_delete= models.SET_NULL)
    name = models.CharField(max_length=200)
    ids = models.PositiveIntegerField()
    def __str__(self):
        return str(self.name)

class videoStore(models.Model):
    User = models.ForeignKey(User, null=True ,  on_delete= models.SET_NULL)
    videoFile = models.FileField(null=True)
    def __str__(self):
        return str(self.User)


class ymlfile(models.Model):
    User = models.ForeignKey(User, null=True ,  on_delete= models.SET_NULL)
    xmlfile = models.FileField(null=True)
    def __str__(self):
        return str(self.User)