from django.db import models

# Create your models here.

class TargetData(models.Model):
    target_name = models.CharField(max_length=100)
    target_id = models.CharField(max_length=300)
    target_recognition_image = models.CharField(max_length=1300)
    target_text = models.CharField(max_length=400)
    target_image = models.CharField(max_length=1300)
    target_3d_model = models.CharField(max_length=50)

class SearchTargetData(models.Model):
    targetid = models.CharField(max_length=300)
