from django.db import models

# Create your models here.
class Customer(models.Model):
	Email = models.EmailField(max_length=200, primary_key=True)
	Password = models.CharField(min_length=200)
	FName = models.CharField(max_length=50)
	LName = models.CharField(max_length=50)