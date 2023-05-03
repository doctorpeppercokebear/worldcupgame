from django.db import models

class User(models.Model):
  email = models.CharField(max_length=50)
  pwd = models.CharField(max_length=100)
  name = models.CharField(max_length=10)

class App(models.Model):
  category = models.CharField(max_length=10, null=True)
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=1000)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(null=True, auto_now=True)

class App2(models.Model):
  category = models.CharField(max_length=10, null=True)
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=1000)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(null=True, auto_now=True)
