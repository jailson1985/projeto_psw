from rest_framework import serializers
from .models import Brewery, ModelContagemCervejaria

class BrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = '__all__'  # ou você pode definir quais campos incluir

class ModelContagemCervejariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelContagemCervejaria
        fields = '__all__'