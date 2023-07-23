from asyncio.windows_events import selector_events
import imp
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
import mysql.connector
import json
from datetime import datetime

from .files import *
from main.mail import send_mail
# Create your views here.
def index(request,*args,**kwargs):
    return render(request,'index.html')

def login(request,*args,**kwargs):
    if request.method=="POST":
            name=request.POST['name']
            password=request.POST['password']
            user=auth.authenticate(username=name,password=password)
            if user is not None: #if user id and password is same
                auth.login(request,user)
                return redirect('p_home')
            else:
                messages.info(request,'invalid credentials')
                return render(request,"login.html")   
    return render(request,'login.html')

def register(request,*args,**kwargs):
    if(request.method == 'POST'):
        name=request.POST['name'] #gets value from the frontend 
        password=request.POST['password']
        if User.objects.filter(username=name).exists(): #checks if the user requests
             messages.info(request,'Username Taken')
             return render(request,'register.html')  #redirects the register page again
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save() #its saves the users id and password in the databasse
            return render(request,'login.html')
    return render(request,'register.html')  

def p_home(request,*args,**kwargs):
    return render(request,'p_home.html')

def p_details(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    if(request.method=='POST'):
        db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
        cur = db.cursor()
        cur.execute("select username from auth_user where id=%s",(request.user.id,))
        s=cur.fetchall()
        name=s[0][0]
        gender=request.POST['gender'] #gets value from the frontend 
        age=request.POST['age']
        address=request.POST['address'] #gets value from the frontend 
        contact_no=request.POST['contact_no']
        email=request.POST['email']
        dob=request.POST['dob']
        cur.execute("select * from patient")
        s=cur.fetchall()
        x=s[len(s)-1][0]+1
        cur.execute("insert into patient values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(x,name,gender,age,dob,address,contact_no,email,0,))
        db.commit()

        return redirect('p_home')
    
    return render(request,'p_details.html')

def book_appointment(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("select * from specialization")
    s=cur.fetchall()
    if(request.method == 'POST'):
        sid=request.POST['consultant']
        mode=request.POST['mode']
        cur.execute("select d.d_id,d_name,s_name,d.time from doctor d,specialization s where d.s_id=s.s_id and d.s_id=%s and mode=%s and availability=%s",(sid,mode,1))
        temp=cur.fetchall()
        
        my_dicti={'val':s,'auxi':temp}
        return render(request,"book_appointment.html",my_dicti)
        
    
    my_dicti={'val':s}
    print(s)
    return render(request,"book_appointment.html",my_dicti)

def b_appointment(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("select username from auth_user where id=%s",(request.user.id,))
    s=cur.fetchall()
    p_name=s[0][0]
    d_name=request.POST['d_name']
    sp=request.POST['sp']
    time=request.POST['time']
    
    print(p_name,d_name,sp,time)
    cur.execute("select d_id from doctor where d_name=%s",(d_name,))
    s=cur.fetchall()
    d_id=s[0][0]
    cur.execute("select patient_id from patient where patient_name=%s",(p_name,))
    s=cur.fetchall()
    p_id=s[0][0]
    print(d_id,p_id)
    date=datetime.date(datetime.now())
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    cur.execute("select * from requests")
    s=cur.fetchall()
    x=s[len(s)-1][0]+1
    cur.execute("insert into requests values(%s,%s,%s,%s,%s,%s,%s,%s)",(x,d_id,p_id,date,time,2,"NONE","NONE"))
    db.commit()
    return render(request,"p_home.html")
    

def d_register(request,*args,**kwargs):
    if(request.method == 'POST'):
        name=request.POST['name'] #gets value from the frontend 
        password=request.POST['password']
        if User.objects.filter(username=name).exists(): #checks if the user requests
             messages.info(request,'Username Taken')
             return render(request,'d_register.html')  #redirects the register page again
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save() #its saves the users id and password in the databasse

            return render(request,'d_login.html')
    return render(request,'d_register.html')  

def d_login(request,*args,**kwargs):
    if request.method=="POST":
            name=request.POST['name']
            password=request.POST['password']
            user=auth.authenticate(username=name,password=password)
            if user is not None: #if user id and password is same
                auth.login(request,user)
                return redirect('d_home')
            else:
                messages.info(request,'invalid credentials')
                return render(request,"d_login.html")   
    return render(request,'d_login.html')

def d_home(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("update auth_user set is_staff=1 where id=%s",(request.user.id,))
    db.commit()
    return render(request,"d_home.html")

def pres_medicine(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("select username from auth_user where id=%s",(request.user.id,))
    s=cur.fetchall()
    d_name="Dr."+s[0][0]
    cur.execute("select d_id from doctor where d_name=%s",(d_name,))
    s=cur.fetchall()
    doctor_id=s[0][0]
    none_="NONE"
    cur.execute("select * from requests where d_id=%s and prescription=%s",(doctor_id,none_))
    s=cur.fetchall()
    print(s)
    list_1=[]
    for i in range(len(s)):
        p_id=s[i][2]
        cur.execute("select patient_name from patient where patient_id=%s",(p_id,))
        x=cur.fetchall()
        p_name=x[0][0]
        my_str=str(s[i][0])+" "+p_name+" "+s[i][3]+" "+s[i][4]
        list_1.append(my_str)
    if request.method=="POST":
        a_details=request.POST['a_details'] #gets value from the frontend 
        presc=request.POST['presc']
        id=int(a_details[0])
        auxi=a_details.split()
        time=auxi[len(auxi)-1]
        date=auxi[len(auxi)-2]
        cur.execute("update requests set prescription=%s where r_id=%s and date=%s and time=%s",(presc,id,date,time))
        db.commit()
        print(a_details,presc)
        return render(request,"d_home.html")
    my_dicti={"val":list_1}
    return render(request,"presc.html",my_dicti)

def p_reports(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("select username from auth_user where id=%s",(request.user.id,))
    s=cur.fetchall()
    p_name=s[0][0]
    print(p_name)
    none_="NONE"
    cur.execute("select d.d_name,r.date,r.time,s.s_name,r.prescription from requests r,doctor d,patient p,specialization s where r.p_id=p.patient_id and r.d_id=d.d_id and r.prescription!=%s and p.patient_name=%s and d.s_id=s.s_id",(none_,p_name))
    s=cur.fetchall()
    my_dicti={"val":s}
    print(s)
    if request.method=="POST":
        time=request.POST['time']
        date=request.POST['date']
        cur.execute("select d.d_name,s.s_name,r.prescription,r.report from requests r,doctor d,patient p,specialization s where r.p_id=p.patient_id and r.d_id=d.d_id and r.prescription!=%s and p.patient_name=%s and d.s_id=s.s_id and r.date=%s and r.time=%s",(none_,p_name,date,time))
        s=cur.fetchall()
        print(s)
        d_name=s[0][0]
        d_spes=s[0][1]
        pres=s[0][2]
        report=s[0][3]

        download_reports(p_name,d_name,d_spes,date,time,pres,report)
        return render(request,"p_reports.html",my_dicti)
    return render(request,"p_reports.html",my_dicti)

def m_order(request,*args,**kwargs):        
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("select * from medicine")
    s=cur.fetchall()
    my_dicti={"auxi":s}
    if request.method=="POST":
        send_mail(10000,"John")
        return render(request,"p_home.html",my_dicti)

    return render(request,"m_order.html",my_dicti)

def a_login(request,*args,**kwargs):
    if request.method=="POST":
            name=request.POST['name']
            password=request.POST['password']
            user=auth.authenticate(username=name,password=password)
            if user is not None: #if user id and password is same
                auth.login(request,user)
                return redirect("a_home")
            else:
                messages.info(request,'invalid credentials')
                return render(request,"a_login.html")  
    return render(request,"a_login.html")

def a_register(request,*args,**kwargs):
    if(request.method == 'POST'):
        name=request.POST['name'] #gets value from the frontend 
        password=request.POST['password']
        if User.objects.filter(username=name).exists(): #checks if the user requests
             messages.info(request,'Username Taken')
             return render(request,'a_register.html')  #redirects the register page again
        else:
            user = User.objects.create_user(username=name, password=password)
            user.save() #its saves the users id and password in the databasse

            return render(request,'a_login.html')
    return render(request,"a_register.html")

def a_home(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("update auth_user set is_staff=2 where id=%s",(request.user.id,))
    db.commit()
    if(request.method == 'POST'):
        billing()
        print("not downloading")
        return render(request,"a_home.html")

    return render(request,"a_home.html")


def update_patient(request,*args,**kwargs):
    db = mysql.connector.connect(host="34.93.148.237",user="root",password="1234",database="Hackathontyl") 
    cur = db.cursor()
    cur.execute("select * from patient")
    s=cur.fetchall()
    my_dicti={"val":s}
    return render(request,"update_patient.html",my_dicti)






