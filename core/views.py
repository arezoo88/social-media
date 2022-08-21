from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Profile
import cloudinary.uploader

User = get_user_model()


@login_required(login_url='core:signin')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='core:signin')
def settings(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            profile_image = user_profile.profile_image

        else:
            image = request.FILES.get('image')
            uploaded_file = cloudinary.uploader.upload(image, use_filename=True, folder='profile_image', public_id=str(user_profile.id_user),
                                                       overwrite=True, invalidate=True)
            profile_image = "v" + \
                str(uploaded_file['version'])+"/"+uploaded_file['public_id']
        user_profile.profile_image = profile_image
        bio = request.POST['bio']
        location = request.POST['location']
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('core:settings')

    return render(request, 'setting.html', {'user_profile': user_profile})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken!')
                return redirect('core:signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('core:signup')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                user_login = auth.authenticate(
                    username=username, password=password)
                auth.login(request, user_login)
                return redirect('core:settings')

        else:
            messages.info(request, 'Password Not Matching!')
            return redirect('core:signup')

    return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credential Invalid!')
            return redirect('core:signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='core:signin')
def logout(request):
    auth.logout(request)
    return redirect('core:signin')
