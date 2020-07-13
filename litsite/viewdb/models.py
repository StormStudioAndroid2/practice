from django.db import models

# Create your models here.
class Books(models.Model):
    author = models.CharField(max_length=200, default = "",blank=True)
    publisher = models.CharField(max_length=200, default = "",blank=True)
    title = models.CharField(max_length=200, default = "",blank=True)
    def __str__(self):
        return self.title
    