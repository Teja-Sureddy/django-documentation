from django.db import models
from rest_framework import serializers


class TempModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='temp/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TempModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempModel
        fields = ['id', 'title', 'description', 'image', 'created_at']


##########################################################################

class TempModel2(models.Model):
    temp_model = models.ForeignKey(TempModel, on_delete=models.CASCADE)
    comment = models.TextField()


class TempModel2Serializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='rest_framework:class_api_pk_view', lookup_field='pk')
    temp_model_url = serializers.HyperlinkedIdentityField(view_name='rest_framework:class_generic_pk_view',
                                                          lookup_field='pk')
    temp_model = serializers.PrimaryKeyRelatedField(queryset=TempModel.objects.all())

    class Meta:
        model = TempModel2
        fields = ['url', 'temp_model_url', 'temp_model', 'comment']
