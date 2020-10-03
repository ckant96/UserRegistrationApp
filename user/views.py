from django.shortcuts import render
from django.http import  HttpResponse
from django.http import  HttpResponseRedirect
from django.template import  loader
from django.db import connection
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        authent = authenticate(username=username,password=password)
        if  authent:
            with connection.cursor() as cursor:
                cursor.execute("SELECT  name FROM User where user_id=%s and password=%s", [username, password])
                row = cursor.fetchall()
                if row :
                    login(request,authent)
                    return render(request=request, template_name="UserPage.html", context={'Status': 'successful','userId':'Invalid Credentials'})
                else:
                    return render(request=request, template_name="Login.html",context={'Status': 'Unsuccessful','userId':'Invalid Credentials'})
        else:
            return render(request, 'Login.html', {'Status': 'Unsuccessful','userId':'Invalid Credentials'})
    return render(request=request, template_name="Login.html", context={'Status': 'Unsuccessful','userId':'Invalid Credentials'})

def UserRegister(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        upass = request.POST.get('password')
        cname = request.POST.get('confirm_password')
        if not uname or not upass or not cname  :
            return render(request=request, template_name="Registration.html",context={'Status':'Invalid entries'})
        if uname != cname  :
            return render(request=request, template_name="Registration.html",context={'Status':'Password Mismatch.'})

        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM auth_user where username = %s ",[uname])
            already=cursor.fetchall()

        if already :
            return render(request=request, template_name="Registration.html",context={'Status':'UserName Exists.'})
        else:
            with connection.cursor() as cursor:
                    cursor.execute("INSERT into User (username,password) VALUES(%s,%s)", [uname, upass])
            User.objects.create_user(uname,None,upass)
            return render(request=request, template_name="Registration.html",context={'Status': 'account Created'})

    return render(request=request, template_name="Registration.html" , context={'Status': 'account Creation failed'})

@login_required()
def SaveUserNote(request,userId):
    if request.method == 'POST':
        notes = request.POST.get('user_notes')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from UserNotes where username= %s ", [userId])
            row = cursor.fetchall()
            if row :
                newnote=row[0]+notes # append new note to old note string
                cursor.execute(" UPDATE UserNotes set notes=%s",[newnote])
            else:
                cursor.execute(" INSERT into UserNotes(userId,notes) VALUES(%s,%s)", [userId,notes])
        return render(request=request, template_name="UserNotes.html" , context={'Status': 'Success'})
    return render(request=request, template_name="UserNotes.html" , context={'Status': 'UnSuccess'})


@login_required()
def ShowUserNote(request,userId):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from UserNotes where username= %s ", [userId])
            row = cursor.fetchall()
            note_list=[]
            if row :
                note_list = row[0].split('+')
        return render(request=request, template_name="UserNotes.html" , context={'Notes': note_list})


