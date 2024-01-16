from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url= '/')
def receipes(request):
    if request.method == "POST":
        data = request.POST

        receipy_name = data.get('receipy_name')
        receipy_description = data.get('receipy_description')
        receipy_image = request.FILES.get('receipy_image')

        Receipy.objects.create(
            receipy_name = receipy_name,
            receipy_description = receipy_description,
            receipy_image = receipy_image,
        )

        return redirect('/receipes')
        
    queryset = Receipy.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(receipy_name__icontains = request.GET.get('search'))

    context = {'receipes': queryset}
    return render(request, 'receipes.html', context)

@login_required(login_url= '/')
def delete_receipe(request , id):

    queryset = Receipy.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes')

@login_required(login_url= '/')
def update_receipe(request , id):
    queryset = Receipy.objects.get(id = id)

    if request.method == "POST":
        data = request.POST

        receipy_name = data.get('receipy_name')
        receipy_description = data.get('receipy_description')
        receipy_image = request.FILES.get('receipy_image')

        queryset.receipy_description = receipy_description
        queryset.receipy_name = receipy_name

        if receipy_image:
            queryset.receipy_image = receipy_image
        queryset.save()

        return redirect('/receipes')

    context = {'Receipy' : queryset}
    return render(request, 'update_receipes.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
       

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'User not exist')
            return redirect('/')
        user = authenticate(username = username , password = password)

        if user is None:
            messages.info(request, 'Invalid Password')
            return redirect('/')
        else:
            login(request,user)
            return redirect('/receipes')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request,'User already exists')
            return redirect('/register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.info(request,'Account created successfully')
        return redirect('/')

    return render(request, 'register.html')
