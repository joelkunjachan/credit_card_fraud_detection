from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from  django.core.files.storage import FileSystemStorage
import datetime

from .models import *
import os
import json
import csv
import io

from ML import credit_credit


def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')

        reg=registerr(name=name,email=email,password=password)
        reg.save()
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if email == 'admin@gmail.com' and password =='admin':
        request.session['logintdetail'] = email
        request.session['admin'] = 'admin'
        return render(request,'index.html')

    elif registerr.objects.filter(email=email,password=password).exists():
        userdetails=registerr.objects.get(email=request.POST['email'], password=password)
        if userdetails.password == request.POST['password']:
            request.session['uid'] = userdetails.id
        
        return render(request,'index.html')
        
    else:
        return render(request, 'login.html', {'success':'Invalid email id or Password'})
    
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)

def v_users(request):
    user = registerr.objects.all()
    return render(request, 'viewusers.html', {'result': user})

def test(request):
    return render(request,'test.html')

def addfile(request):
    if request.method=="POST":
        u_id = request.session['uid']
        
        file = request.FILES['file']
        
        # Extract CSV data and convert to JSON
        file.seek(0)  # Reset file pointer
        csv_data = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
        data_list = list(csv_data)
        json_data = json.dumps(data_list)
        
        result = credit_credit.predict(data_list)

        cus=uploads(u_id=u_id,result=result,data=json_data)
        cus.save()
        return render(request,'test.html',{'result':result})
    return render(request,'test.html')
    
def v_result(request):
    uid=request.session['uid']
    user = uploads.objects.filter(u_id=uid)
    return render(request, 'viewresult.html', {'result': user})

def view_results(request):
    # Only show transactions flagged as fraudulent (result = "0")
    fraudulent_transactions = uploads.objects.filter(result="0")
    return render(request, 'viewresult.html', {'result': fraudulent_transactions})

def live(request):
    return render(request,'live.html')

# Staff Views
def staff_register(request):
    return render(request,'staff_register.html')

def staff_registration(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        department=request.POST.get('department', 'Fraud Review')

        staff_reg=staff(name=name,email=email,password=password,department=department)
        staff_reg.save()
    return render(request,'staff_login.html')

def staff_login(request):
    return render(request,'staff_login.html')

def staff_addlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    if staff.objects.filter(email=email,password=password).exists():
        staff_details=staff.objects.get(email=email, password=password)
        if staff_details.password == password:
            request.session['staff_id'] = staff_details.id
            request.session['staff_name'] = staff_details.name
            request.session['staff_email'] = staff_details.email
            return redirect('staff_dashboard')
    return render(request, 'staff_login.html', {'error':'Invalid email or password'})

def staff_dashboard(request):
    if 'staff_id' not in request.session:
        return redirect('staff_login')

    # Get all transactions flagged as fraudulent (result="0")
    fraudulent_transactions = uploads.objects.filter(result="0").order_by('-id')
    return render(request, 'staff_dashboard.html', {'transactions': fraudulent_transactions})

def staff_logout(request):
    if 'staff_id' in request.session:
        del request.session['staff_id']
        del request.session['staff_name']
        del request.session['staff_email']
    return redirect('staff_login')

def review_transaction(request, transaction_id):
    if 'staff_id' not in request.session:
        return redirect('staff_login')

    transaction = uploads.objects.get(id=transaction_id)

    if request.method == "POST":
        action = request.POST.get('action')
        review_notes = request.POST.get('review_notes', '')

        if action == 'approve':
            transaction.status = 'approved'
        elif action == 'block':
            transaction.status = 'blocked'

        transaction.staff_review = review_notes
        transaction.reviewed_by = request.session['staff_name']
        from django.utils import timezone
        transaction.reviewed_at = timezone.now()
        transaction.save()

        return redirect('staff_dashboard')

    return render(request, 'review_transaction.html', {'transaction': transaction})