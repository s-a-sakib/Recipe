from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Receipy(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipy_name = models.CharField(max_length= 100)
    receipy_description = models.TextField()
    receipy_image = models.ImageField(upload_to= "receipy")







    