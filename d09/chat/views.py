from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Room

def room_list_view(request):
    # DBにあるRoomを全て表示してリンク化する
    rooms = Room.objects.all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})

@login_required
def room_detail_view(request, slug):
    # ログイン必須 (未ログインならログインページへリダイレクト)
    # slug is unique to each room
    room = get_object_or_404(Room, slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})
