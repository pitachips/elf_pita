from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#from django.contrib.auth.forms import UserCreationForm
from accounts.forms import SignupForm1, SignupForm2
from accounts.models import UserProfile

from legolas.models import Review

# Create your views here.


def signup1(request):
    if request.method == 'POST':
        form = SignupForm1(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return redirect('/accounts/signup2')
    else:
        form = SignupForm1()
    return render(request, 'accounts/signup1.html', {'form':form})


def signup2(request):
    if request.method == 'POST':
        form = SignupForm2(request.POST)
        if form.is_valid():
            new_user_profile = form.save(commit=False)
            new_user_profile.user = request.user
            new_user_profile.save()
            messages.info(request, "You are so much welcome!")
            return redirect('/accounts/profile')
    else:
        form = SignupForm2()
    return render(request, 'accounts/signup2.html', {'form':form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')



def user_detail(request, pk):
    a_user = get_object_or_404(User, pk=pk)
    users_reviews = Review.objects.filter(author=a_user).order_by('-created_at')

    return render(request, 'accounts/user_detail.html', {'a_user': a_user, 'users_reviews':users_reviews})


def user_detail_follower(request, pk):
    pass


def user_detail_following(request, pk):
    pass


def user_detail_bookmark(request, pk):
    pass
