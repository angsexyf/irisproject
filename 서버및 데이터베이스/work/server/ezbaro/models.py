from django.db import models

class Data(models.Model):
    content = models.TextField(verbose_name="컨텐츠")
    content_type = models.CharField(max_length=50, primary_key=True)
# Create your models here.
