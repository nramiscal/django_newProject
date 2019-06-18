from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
    else:
        request.session['gold'] += 1

    return render(request, "index.html")

def register_owner(request):
    print("1. inside views.py register_owner method")
    errors = Owner.objects.registerValidator(request)
    print("4. back inside views.py register_owner method")
    print("5.", errors)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        # create owner in database
        hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        # print(hash)
        # print(hash.decode())

        owner = Owner.objects.create(fname=request.POST["fname"], lname=request.POST["lname"], email=request.POST["email"],password=hash.decode())
        # store id in session
        request.session['id'] = owner.id
        return redirect("/success")

def success(request):
    logged_in_user = Owner.objects.get(id=request.session['id'])
    return render(request, "success.html", {'fname': logged_in_user.fname})
