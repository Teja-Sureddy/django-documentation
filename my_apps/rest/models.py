from django.db import models
from rest_framework import serializers


class Temp1(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='temp/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Temp1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Temp1
        fields = ['id', 'title', 'description', 'image', 'created_at']


##########################################################################

class Temp2(models.Model):
    temp_model = models.ForeignKey(Temp1, on_delete=models.CASCADE)
    comment = models.TextField()


class Temp2Serializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='rest_framework:class_api_pk_view', lookup_field='pk')
    temp_model_url = serializers.HyperlinkedIdentityField(view_name='rest_framework:class_generic_pk_view',
                                                          lookup_field='pk')
    temp_model = serializers.PrimaryKeyRelatedField(queryset=Temp1.objects.all())

    class Meta:
        model = Temp2
        fields = ['url', 'temp_model_url', 'temp_model', 'comment']
