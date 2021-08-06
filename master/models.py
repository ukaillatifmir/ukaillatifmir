from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

#...........USER MODEL...........
choice=(('male','male'),('female','female'))
class Registeration(models.Model):
    user_name=models.CharField(max_length=20,blank=True)
    last_name=models.CharField(max_length=20,blank=True)
    Gender=models.CharField(max_length=20,blank=True,choices=choice)
    class Meta:
        abstract=True

class user(Registeration):
    Email=models.EmailField(max_length=20,blank=False,primary_key=True)
    password=models.CharField(max_length=20,blank=False)
    last_login=models.DateTimeField(blank=True,null=True)
    login_successful=models.IntegerField(default=0)
    timestamp=models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.Email


#......BUSINESS CARD..................
class business_card(models.Model):
    email=models.ForeignKey(user,blank=True,unique=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=False)
    phone=models.CharField(max_length=50,blank=False)

#....POST MODEL..............



#.....THIS MODEL CONTAINS FRONT COVER .......
class cover(models.Model):
    email=models.ForeignKey(user,blank=True,on_delete=models.CASCADE)
    images=models.ImageField(blank=True, null=True) # POST TAGS REPLACE TO IMAGES
    discription=models.CharField(max_length=300,blank=True) # POST NAME AND POST CONTENT IS REPLACED WITH DISCRIPTION
    timestamp=models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.id)




#...THIS  MODEL CONTAINS ALL POST TAGS ..................... 
class post(models.Model):
    link=models.ForeignKey(cover,blank=True,on_delete=models.CASCADE)
    all_images=models.ImageField(blank=True, null=True) 
    


