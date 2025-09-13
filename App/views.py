from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

from .models import UserPredictModel,Patient_info

from tensorflow import keras
from PIL import Image, ImageOps
from . import forms


import serial
import time
import re

ser = serial.Serial()
ser.port = 'COM8'
ser.baudrate = 9600
ser.bytesize = 8
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE

def serialget():
    value=[]
    ser.open()
    time.sleep(1)
    v=b'C'
    ser.write(v)
    while True:
        for line in ser.read():
            if chr(line) != '$':
                value.append(chr(line))
            else:
                print("end")
                ser.close()
                return value


def request(request):
    str1=''
    val=[]
    va=serialget()
    print(va)
    for v in va:
        if(v== '*'):
            continue
        else:  
            if(v!='#'): 
                str1+=v
            else:
                print(str1)
                cleaned_str = re.sub(r'[^0-9.,]', '', str1)
                try:
                    val = [float(num) for num in cleaned_str.split(',')]
                except ValueError:
                    print(f"Error converting {cleaned_str} to float.")
                str1=""   
    return render(request, 'app/9_Deploy.html', {'val1':int(val[0])})


def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

from .models import Profile

def profile(request):
    user = request.user
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


Model1 = joblib.load('D:/Projects/Nextgen health survaillance/nextgen_health_surveillance_ar_meets_ai_for_predictive_heart_attack_analytics/App/CARDIO.pkl')  
from .forms import Patient_info_Form

def Deploy_9(request):
    if request.method == 'POST':
        form = Patient_info_Form(request.POST)
        if form.is_valid():
            # Extract cleaned data from form
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            chest_pain = form.cleaned_data['chest_pain']
            trestbps = form.cleaned_data['trestbps']
            chol = form.cleaned_data['chol']
            fbs = form.cleaned_data['fbs']
            restecg = form.cleaned_data['restecg']
            thalach = form.cleaned_data['thalach']
            exang = form.cleaned_data['exang']
            oldpeak = form.cleaned_data['oldpeak']
            slope = form.cleaned_data['slope']
            ca = form.cleaned_data['ca']
            thal = form.cleaned_data['thal']
            
            # Prepare features for prediction
            features = np.array([[age, gender, chest_pain, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
         
            
            prediction = Model1.predict(features)
            prediction = prediction[0]   
    
            
            if prediction == 0:
                a="THE CARDIOVASCULAR MIGHT BE LESS CHANCE OF HEART ATTACK"
                ser.open()
                ser.write(b'B')
                ser.close()
            elif prediction == 1:
                a="THE CARDIOVASCULAR MIGHT BE MORE CHANCE OF HEART ATTACK"
                ser.open()
                ser.write(b'A')
                ser.close()
    
            
            # Save data to database
            instance = form.save(commit=False)
            instance.label = a
            instance.save()
            
            # Render output page with prediction result
            return render(request, 'app/5_Teamates.html', {'prediction_text': a})
    else:
        form = Patient_info_Form()
    
    return render(request, 'app/9_Deploy.html', {'form': form})


from .models import Patient_info

def report(request):
    return render(request,'app/report.html')

def patient_list(request):
    patients = Patient_info.objects.all()
    return render(request, 'app/patient_list.html', {'patients': patients})

def database(request):
    models = UserPredictModel.objects.all()
    return render(request, 'app/img_database.html', {'models':models})

def matrix(request):
    return render(request,'app/matrix.html')


def logout_view(request):  
    auth_logout(request)
    return redirect('/')