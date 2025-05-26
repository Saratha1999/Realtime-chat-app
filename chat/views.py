from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Room
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .forms import RoomForm
from .utils import get_private_room_name
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})



@login_required
def room(request, room_name):
    is_dm = room_name.startswith("dm_")

    if is_dm:
        allowed = room_name.replace("dm_", "").split("_")
        if request.user.username.lower() not in allowed:
            return HttpResponseForbidden("You're not allowed to access this DM.")
        room, _ = Room.objects.get_or_create(name=room_name, defaults={'created_by': request.user})
    else:
        room = get_object_or_404(Room, name=room_name)
        if room.allowed_users.exists():
            if request.user not in room.allowed_users.all() and request.user != room.created_by:
                return HttpResponseForbidden("You're not allowed to access this room.")

    messages = Message.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chat/room.html', {
        'room_name': room.name,
        'username': request.user.username,
        'messages': messages,
        'allowed_users': room.allowed_users.all() 
    })



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def room_list(request):
    form = RoomForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        room_name = form.cleaned_data['name']
        room, created = Room.objects.get_or_create(name=room_name, defaults={'created_by': request.user})
        if created:
            room.allowed_users.set(form.cleaned_data['allowed_users'])  # save allowed users
        return redirect('chat_room', room_name=room.name)

    all_rooms = Room.objects.all().order_by('name')
    users = User.objects.exclude(id=request.user.id)  # include users for 1-on-1 list

    return render(request, 'chat/room_list.html', {
        'rooms': all_rooms,
        'form': form,
        'users': users  
    })

@login_required
def delete_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)

    if request.user == room.created_by:
        room.delete()
        return redirect('room_list')
    else:
        return HttpResponseForbidden("You are not allowed to delete this room.")

@login_required
def private_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect('room_list')  # prevent chatting with self

    room_name = get_private_room_name(request.user.username, other_user.username)
    return redirect('chat_room', room_name=room_name)

@login_required
def private_chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/private_chat_list.html', {'users': users})

