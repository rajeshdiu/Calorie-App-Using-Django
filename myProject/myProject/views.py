from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, authenticate, logout
from myProject.forms import *
from django.contrib import messages

from django.contrib.auth import get_user_model
from myApp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage,send_mail
from myProject.settings import EMAIL_HOST_USER
import random
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Sum

def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('mySigninPage')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('mySigninPage')

def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')

from django.db import IntegrityError
from django.contrib import messages

from django.db import IntegrityError

def signupPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                email=form.cleaned_data.get('email')
                activateEmail(request, user, email)
                messages.success(request, 'Registration successful. You are now logged in.')
                UserProfile.objects.create(user=user)
                UserProfile.save()
                return redirect('mySigninPage')
            except IntegrityError:
                messages.error(request, 'Username already exists. Please choose a different username.')
                return render(request, 'signupPage.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'signupPage.html', {'form': form})

def mySigninPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboardPage')
    else:
        form = AuthenticationForm()
    return render(request, 'loginPage.html', {'form': form})


def logoutPage(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('mySigninPage')


def forget_pass(request):
    if request.method == "POST":
        my_email = request.POST.get("email")
        user = Custom_User.objects.get(email = my_email )
        otp = random.randint(111111,999999)
        user.otp_token = otp
        user.save()
        
        sub = f""" Your OTP : {otp}"""
        msg = f"Your OTP is {otp} , Keep it secret "
        from_mail = EMAIL_HOST_USER
        receipent = [my_email]
        print(user)
        print(receipent)
        print(from_mail)
        
        send_mail(
            subject= sub,
            recipient_list= receipent,
            from_email= from_mail,
            message= msg ,
        )
        return render(request,'updatepass.html',{'email':my_email})

    return render(request, "forgetpass.html")

def update_pass(request):
    if request.method=="POST":
        mail = request.POST.get('email') 
        otp = request.POST.get('otp') 
        password = request.POST.get('password') 
        c_password = request.POST.get('c_password') 
        
        print(mail,otp,password,c_password)

        user = Custom_User.objects.get(email=mail)
        print(user)
        if user.otp_token!= otp :
            return redirect('forget_pass')
        
        if password!= c_password:
            return redirect('forget_pass')
        
        user.set_password(password) 
        user.otp_token = None 
        user.save()
        print(user)
        return redirect ('mySigninPage')

    return render(request, 'updatepass.html')

def dashboardPage(request):
    
    return render(request,'dashboardPage.html')


def ProfilePage(request):
    try:
        user_profile = request.user.userprofile 
        consumed_calories = ConsumedCalories.objects.filter(user=request.user)
        total_calories_consumed = consumed_calories.aggregate(total=Sum('calorie_consumed'))['total'] or 0
        
        if user_profile.gender == 'Male':
            bmr = 66.47 + (13.75 * user_profile.weight) + (5.003 * user_profile.height) - (6.755 * user_profile.age)
        else:
            bmr = 655.1 + (9.563 * user_profile.weight) + (1.850 * user_profile.height) - (4.676 * user_profile.age)
        
        context = {
            'user_profile': user_profile,
            'bmr': bmr,
            'consumed_calories': consumed_calories,
            'total_calories_consumed': total_calories_consumed
        }
    except UserProfile.DoesNotExist:
        return HttpResponse("No user")
    
    return render(request, 'profilePage.html', context)


def add_consumed_calories(request):
    if request.method == 'POST':
        form = ConsumedCaloriesForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            item_name = form.cleaned_data['item_name']
            calorie_consumed = form.cleaned_data['calorie_consumed']
            ConsumedCalories.objects.create(user=request.user, date=date, item_name=item_name, calorie_consumed=calorie_consumed)
            return redirect('calorie_summary')
    else:
        form = ConsumedCaloriesForm()
    return render(request, 'add_consumed_calories.html', {'form': form})

def calorie_summary(request):
    user_profile = request.user.userprofile
    
    calorie_summary = ConsumedCalories.objects.values('date').annotate(total_calories=Sum('calorie_consumed'))
    
    for entry in calorie_summary:
        if user_profile.gender == 'Male':
            bmr = 66.47 + (13.75 * user_profile.weight) + (5.003 * user_profile.height) - (6.755 * user_profile.age)
        else:
            bmr = 655.1 + (9.563 * user_profile.weight) + (1.850 * user_profile.height) - (4.676 * user_profile.age)
        entry['required_calories'] = bmr
    
    context = {
        'calorie_summary': calorie_summary
    }
    return render(request, 'calorie_summary.html', context)


def edit_profile(request):
    user_profile = request.user.userprofile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('ProfilePage')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'edit_profile.html', {'form': form})
