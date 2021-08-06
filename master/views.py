from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
import random 
from .models import *
from .decorator import decorator
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.mail import send_mail
from .tasks import user_sleep
from time import sleep
import random
import os 
import json
from completesite.settings import *
from django.core.files.storage import FileSystemStorage
import datetime

# Create your views here.
msg={'message':''}
#..........FOR REGISTERATION...........
class Index(View):  
    def get(self,request):

        return render(request,'registeration.html')
    def post(self,request):
        button=request.POST['sbt']
        if button != "send" :
            user_name=request.POST['user_name']
            last_name=request.POST['last_name']
            email=request.POST['email']
            password=request.POST['password']
            gender=request.POST['gender']
            cont=user.objects.filter(Email=email).count()
            username_check=user.objects.filter(user_name=user_name).count()
            
            if cont==0 and username_check==0:
                request.session['otp']=random.randint(1000,9999)
                request.session['user_name']=user_name
                request.session['last_name']=last_name
                request.session['email']=email
                request.session['password']=password
                request.session['gender']=gender
                
                #send_mail("Email Check","your otp is "+str(request.session['otp']),"kashmirestatebusiness@gmail.com",[email],fail_silently=False,)
            
                return render(request,"registeration.html",{"message":"otp has been sent on your mail  ",'data_ver':'valid','otp':request.session['otp']})
            
        
            
            else:
                message="user already exist change email id or username"
        
        
            return render(request,"registeration.html",{"message":message})
        else:
            otp=request.POST['otp_data']
            if str(request.session['otp']) == otp:
            
                user_name=request.session['user_name']
                password=request.session['password']
                email=request.session['email']
                last_name=request.session['last_name']
                gender=request.session['gender']

                data=user(user_name=user_name,password=password,Email=email,last_name=last_name,Gender=gender)
                data.save()
            
                del request.session['otp']
                del request.session['user_name']
                del request.session['password']
                del request.session['email']
                del request.session['last_name']
                del request.session['gender']
            
                return render(request,"registeration.html",{'message':"user created"})
            else:
                return render(request,'registeration.html',{'message':'otp doesnot match please check ','data_ver':'valid'})




#........FOR LOGIN ..............
class login(View):  
    def get(self,request, **kwargs):
        try:
            if kwargs['my_id']:
                return render(request,'login.html',{'message':"user created "})
        except:
            return render(request,'login.html',)

        
        

    def post(self,request,**kwargs):
        email=request.POST['email']
        password=request.POST['password']
        data=user.objects.filter(Q(Email=email),Q(password=password)).count()    
        if data==1:
            update_details=user.objects.get(Email=email,password=password)
            
            #import pdb;pdb.set_trace()
            request.session['check']=email
            update_details.last_login=datetime.datetime.now()
            update_details.login_successful+=1
            update_details.save()
            message="loged in successfully"  
            return redirect('dash')
        else:
            message=  "invalid user name or password"
        return render(request,"login.html",{"data":message})

#.....DASHBOARD.............
@method_decorator(decorator,name='dispatch')
class dash(View):
    def get(self,request):
        #import pdb;pdb.set_trace()
        #data=business_card.objects.filter(email=request.session.get('check')
        data=business_card.objects.filter(email=request.session.get('check'))
        DATA=cover.objects.filter(email=request.session.get('check'))[::-1]
        
        if data.count()==0:
            pass
        else:
            record=data.get()
            lst=record.email
            
        

        
        
    
            return render(request,"dash.html",{'fulldetails':record,'DATA':DATA})
        
        return render(request,"dash.html",{'data':request.session.get('check'),'DATA':DATA}) 



# ............... LOGOUT..................
@method_decorator(decorator,name='dispatch')   
class logout(View):
 def get(self,request,*args,**kwargs):  
    #import pdb;pdb.set_trace()  
    del request.session['check']
    return redirect('Home')


#..............FOR BUSINESS CARD MAKING ........................    
@method_decorator(decorator,name='dispatch')  
class businesscard(View):
    def get(self,request):
        #import pdb;pdb.set_trace() 
        
        data=business_card.objects.filter(email=request.session.get('check'))
        if data.count()==0:
            pass
        else:
            record=data.get()
            lst=record.email
            


        
        
    
            return render(request,"card.html",{'fulldetails':record})
        return render(request,"card.html",{'data':request.session.get('check')}) 
    
    def post(self,request):
        name=request.POST['name']
        phone=request.POST['phone']
        #import pdb;pdb.set_trace()
        check=business_card.objects.filter(email=request.session.get('check')).count()
        if check==0:
            data=user.objects.filter(Email=request.session.get('check'))
            record=business_card(email=data.get(),name=name,phone=phone)
            record.save() 
            info=business_card.objects.get(email=request.session.get('check'))
        else:
            data=user.objects.filter(Email=request.session.get('check'))
            info=business_card.objects.get(email=data.get())
            info.name=name
            info.phone=phone
            info.save()
        



        
        
        return render(request,"card.html",{'fulldetails':info})
        
            


        
        
        
        


#...........GENERAL HOMEPAGE .....................
class Home(View):
    def get(self,request):
        #import pdb;pdb.set_trace()
        #data=business_card.objects.filter(email=request.session.get('check')
        
        DATA=cover.objects.all()[::-1]
        return render(request,"home.html",{'DATA':DATA})
        
        
# .............. IMAGE POST..................
@method_decorator(decorator,name='dispatch')  
class imagepost(View):
    
    def get(self,request):
        #import pdb;pdb.set_trace() 
        
        data=business_card.objects.filter(email=request.session.get('check'))
        if data.count()==0:
            pass
        else:
            record=data.get()
            lst=record.email
            return render(request,"dash.html",{'fulldetails':record,'image_form':'open'})
        return render(request,"dash.html",{'data':request.session.get('check'),'image_form':'open'})


    def post(self,request):
        
        file_name=request.FILES.getlist('image')
        disc=request.POST.get('disc')
        fact=0
        
        for image in file_name:
            if str(image).endswith(('.jpg','.png','.jpeg')):
                pass
            else:
                fact=1
        #import pdb;pdb.set_trace()
                
                
        if fact==0:
            #import pdb;pdb.set_trace()
            fs = FileSystemStorage()
            #today = datetime. datetime. now()
            date_time = random.randint(1000,9999)
            file = fs.save(str(date_time)+file_name[0].name, file_name[0])
            fileurl = fs.url(file)

            login_instance=user.objects.get(Email=request.session.get('check'))
            data=cover.objects.create(images=str(date_time)+file_name[0].name,discription=disc,email=login_instance)
            data.save()
            for img in file_name:
                date_time = random.randint(1000,9999)
                file = fs.save(str(date_time)+img.name, img)
                fileurl = fs.url(file)
                dt_image=post.objects.create(all_images=str(date_time)+img.name,link=data)
                dt_image.save()
            


            return render(request,"dash.html",{'post_message':" POST SUCCESSFULLY UPLOADED SEE IT ON YOUR DASHBOARD ",'image_form':'open'})

        else:
            return render(request,'dash.html',{'post_message':" It Will only Accept JPG JPEG PNG Formats ! MAKE SURE ALL FILES COMES UNDER THESE FORMATS ",'image_form':'open'})
@method_decorator(decorator,name='dispatch')  
class inner(View):
    def get(self,request ,my_id):
        #import pdb;pdb.set_trace()
        try:
            data=business_card.objects.filter(email=request.session.get('check'))
        
            all_posts=post.objects.filter(link=my_id)
            all_dis=cover.objects.filter(id=my_id)



            if data.count()==0:

                pass
            else:
                record=data.get()
                lst=record.email
                return render(request,"inner.html",{'fulldetails':record,'inner_details':all_posts,'disc':all_dis[0]})
            return render(request,"inner.html",{'data':request.session.get('check'),'inner_details':all_posts,'disc':all_dis[0]})
        except:
            return render(request,"error.html")
    def post(self,request,my_id):
        
        all_posts=post.objects.filter(link=my_id)
        all_dis=cover.objects.filter(id=my_id)
        os.remove(all_dis[0].images.path)
        for item in all_posts:
            os.remove(item.all_images.path)
        
        all_dis.delete()

        return HttpResponse(str(" POST DELETED <a href='dash'> GO TO DASHBOARD</a> "))


class homeinner(View):
    def get(self,request ,my_id):
        
        
        all_posts=post.objects.filter(link=my_id)
        all_dis=cover.objects.filter(id=my_id)



        
        return render(request,"homeinner.html",{'inner_details':all_posts,'disc':all_dis[0]})