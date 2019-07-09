from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .models import Photo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from .forms import PhotoForm
from django.contrib import messages
from django.views.decorators.http import require_POST 

def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'photo_app/index.html', {'photos': photos})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'photo_app/users_detail.html', {'user': user, 'photos': photos})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # ユーザーインスタンスを作成
        if form.is_valid():
            new_user = form.save() # ユーザーインスタンスを保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
              login(request, new_user)
              return redirect('photo_app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'photo_app/signup.html', {'form': form})

@login_required
def photos_new(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, "投稿が完了しました！") 
        return redirect('photo_app:users_detail', pk=request.user.pk)
    else:   
        form = PhotoForm()
    return render(request, 'photo_app/photos_new.html', {'form': form})

def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo_app/photos_detail.html', {'photo': photo})

@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('photo_app:users_detail', request.user.id)
# Create your views here.
