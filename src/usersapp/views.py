from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy



# Create your views here.
def main(request):
    return render(request=request, template_name='usersapp/index.html', context={})


def create_user_profile(request):
    if request.user.is_authenticated:
        return redirect('usersapp:main')

    if request.method == 'POST':
        form = forms.CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usersapp:login_user')
        else:
            return render(request, 'usersapp/signup.html', context={"form": form})

    form = forms.CustomUserRegisterForm()
    return render(request, 'usersapp/signup.html', context={"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(to='usersapp:main')

    if request.method == 'POST':
        print('I\'m in POST')
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            print('I\'m in POST but user is NONE ')
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='usersapp:login_user')

        login(request, user)
        print("You was Logged IN !!!!!!!!!!!!!!!")
        return redirect(to='usersapp:main')

    form = forms.LoginForm()
    return render(request, 'usersapp/login.html', context={"form": form})


@login_required
def logout_user(request):
    logout(request)
    return redirect(to='usersapp:main')



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'usersapp/password_reset.html'
    email_template_name = 'usersapp/password_reset_email.html'
    html_email_template_name = 'usersapp/password_reset_email.html'
    success_url = reverse_lazy('usersapp:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'usersapp/password_reset_subject.txt'