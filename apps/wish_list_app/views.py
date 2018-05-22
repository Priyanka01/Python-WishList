from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages


def index(request):
    if 'userid' in request.session:
        del request.session['userid']
    return render(request,"wish_list_app/index.html")
def sucess(request):
    return render(request,"wish_list_app/sucess.html")

def register(request):
    if request.method == 'POST':
        result = User.objects.insertuser(request.POST)
        if 'user' in result:
            request.session['userid'] = result['user'].id
            return redirect("/dashboard")
        else:
            for keys in result:
                messages.error(request, result[keys])
            return redirect("/")
    return redirect("/")

def login(request):
    if request.method == 'POST':
        result = User.objects.validate_login(request.POST)
        if 'user' in result:
            request.session['userid'] = result['user'].id
            return redirect('/dashboard')
        else:
            messages.error(request,result['login'])
            return redirect("/")
    return redirect("/")

def logout(request):
    if 'userid' in request.session:
        request.session.clear()
    return redirect("/") 

#Dashboard
def dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])

    myitems = user.added_items.all()
    otheritems = List.objects.exclude(added_by_users=user)

    to_html = {
        'user': user,
        'myitems': myitems,
        'otheritems': otheritems
    }
    return render(request,"wish_list_app/dashboard.html",{'to_html':to_html})

def additem(request):
    return render(request,"wish_list_app/additem.html")

# Delete item from database
def deleteitem(request,itemid):
    list_rec= List.objects.get(id = itemid).delete()
    return redirect("/dashboard")

# Create new item in db    
def createItem(request):
    if request.method == 'POST':
        result = List.objects.createItem(request.POST,request.session['userid'])    
    if 'list' in result:
        return redirect('/dashboard') 
    else:
        for keys in result:
            messages.error(request, result[keys])
        return render(request,"wish_list_app/additem.html")
    return redirect('/dashboard')         

#Add item from other users to my list
def addthistomylist(request,itemid):
    if 'userid' not in request.session:
        return redirect('/')
    result = List.objects.addItem(itemid, request.session['userid'])
    if 'success' in result:
        return redirect('/dashboard')

#Remove item created by other users from my list
def removethisfrommylist(request,itemid):
    if 'userid' not in request.session:
        return redirect('/')
    result = List.objects.removeItem(itemid, request.session['userid'])
    if 'success' in result:
        return redirect('/dashboard')

#Show item details
def itemdetails(request,itemid):
    list_rec= List.objects.get(id = itemid)
    data = { "itemname": list_rec.item,
    "all_users": list_rec.added_by_users.all()
    }
    return render(request,"wish_list_app/itemdetails.html",{'item':data})    
