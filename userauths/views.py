from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from userauths import forms as userauths_forms
from doctor import models as doctor_models
from patient import models as patient_models
from userauths import models as userauths_models



def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    if request.method == "POST":
        form = userauths_forms.UserRegisterForm(request.POST or None)

        if form.is_valid():
            password1 = form.cleaned_data.get("password1")

            # ---- Custom Password Validation ----
            if password1.isdigit():
                messages.error(request,"Password cannot be only numbers. Please add letters too.")
            else:
                # If password is valid, continue
                user = form.save()
                full_name = form.cleaned_data.get("full_name")
                email = form.cleaned_data.get("email")
                user_type = form.cleaned_data.get("user_type")

                user = authenticate(request, email=email, password=password1)

                if user is not None:
                    login(request, user)

                    if user_type == "Doctor":
                        doctor_models.Doctor.objects.create(user=user, full_name=full_name)
                    else:
                        patient_models.Patient.objects.create(user=user, full_name=full_name, email=email)

                    messages.success(request, "Account created successfully")
                    return redirect("/")
                else:
                    messages.error(request, "Authentication failed, please try again!")
        else:
            # If the form is invalid (e.g., no password, etc.), show the errors
            messages.error(request, "Please correct the errors in the form.")

    else:
        form = userauths_forms.UserRegisterForm()

    context = {
        "form": form
    }
    return render(request, "userauths/sign-up.html", context)



def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")

    if request.method == "POST":
        form = userauths_forms.LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user_authenticate = authenticate(request, email=email, password=password)

                if user_authenticate is not None:
                    # Check if the user is a superuser
                    if user_authenticate.is_superuser:
                        messages.error(request, "Admin users must login through the admin panel.")
                        return redirect("base:sign-in")  # or just reload the page
                        
                    login(request, user_authenticate)

                    messages.success(request, "Logged in successfully")
                    
                    next_url = request.GET.get("next", '/')
                    return redirect(next_url)
                else:
                    messages.error(request, "Invalid username or password!")
            except userauths_models.User.DoesNotExist:
                messages.error(request, "User does not exist!")
    else:
        form = userauths_forms.LoginForm()

    context = {
        "form": form
    }
    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("userauths:sign-in")
