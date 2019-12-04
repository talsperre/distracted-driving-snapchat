from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from authentication.models import OTP
import pyotp


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def homepage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard/instructions')
    return render(request, 'home.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def loginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard/instructions')
    return render(request, 'login.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def navbar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard/instructions')
    return render(request, 'navbar.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def signupPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard/instructions')
    return render(request, 'signup.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def registerUser(request):
    email = request.POST.get('email', '')
    try:
        validate_email(email)
    except:
        return HttpResponse('Invalid email')

    password = request.POST.get('password', '')
    confirmPassword = request.POST.get('confirmPassword')
    print(password)
    print(confirmPassword)
    if (password != confirmPassword):
        return HttpResponse('passwords do not match')

    # firstName = request.POST.get('firstName','')
    # lastName = request.POST.get('lastName','')
    try:
        user = User.objects.create_user(username=email, password=password, email = email)
        totp = pyotp.TOTP('base32secret3232', 6, interval=1)
        otp = totp.now()
        send_mail('Verification code: ' + otp, 'Your verification code is ' + otp + '. Do not share this with anyone',
                  'Snapchat Annotation Portal karan.jkps@gmail.com', [email])
        OTP.objects.create(otp=otp, email=email)
        return render(request, 'OTP.html')
    except:
        return HttpResponse('Email ID already exists')


@csrf_exempt
def verifyOtp(request):
    otp = request.POST.get('OTP','')
    email = request.POST.get('email','')
    otpobj = OTP.objects.filter(email = email).first()
    user = User.objects.filter(email = email).first()
    print(user)
    if not user:
        return HttpResponseRedirect('')
    if not otpobj:
        return HttpResponse('You are already registered. Please Login',status=501)
    if otp != otpobj.otp:
        return HttpResponse('Invalid OTP',status=501)
    else:
        otpobj.delete()
        auth.login(request,user)
        return HttpResponseRedirect('dashboard/instructions')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def loginUser(request):
    username = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('dashboard/instructions')
    else:
        return HttpResponse('password does not match',status=404)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/snap')
