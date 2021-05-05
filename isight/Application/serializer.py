from rest_framework import serializers
from .models import *

class PDFSerializer(serializers.ModelSerializer):
	class Meta:
		model = pdf
		fields ='__all__'



class FacesSerializer(serializers.ModelSerializer):
	class Meta:
		model = FaceName
		fields ='__all__'

class XmlfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ymlfile
		fields ='__all__'