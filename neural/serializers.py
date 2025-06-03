from rest_framework import serializers
from .models import UserImagePost

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImagePost
        fields = ('id', 'image')