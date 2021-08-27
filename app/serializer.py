import jsonfield
from rest_framework import serializers
import jsonfield

class RecomendSerializer(serializers.Serializer):
    
    username=serializers.CharField(max_length=70)
    jsondata=serializers.JSONField()

