from django.shortcuts import render, redirect
from accounts.models import Profile
from .models import Room
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from random import randint
from django.db import transaction
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def NEW(request):
    try:
        pk_list=request.POST.getlist("chk_info[]")
        print(pk_list)
        participants=[request.user, ]

        for name in pk_list:
            participants.append(get_user_model().objects.get(username=name))

    except(KeyError):
        print("비 정상적 행동. 코딩 미스.")
    else:
        S=set(participants)
        candidate_rooms=Room.objects.annotate(c=Count('users')).filter(c=len(S))

        for USER in S:
            candidate_rooms=candidate_rooms.filter(users=USER)

        if(candidate_rooms):
            print("이미 방이 존재하고 있습니다. 채팅방으로 연결해드립니다.")
            #   redirection 시키는 코드 넣을 것.
            return HttpResponseRedirect(reverse('blog:index'))

        #       여기서 새로 방을 만들어준다.
        print("새로운 방을 만듭니다.")

        new_room=None
        while not new_room:
            with transaction.atomic():
                label=randint(1, 10000+1)
                if Room.objects.filter(label=label).exists():
                    continue
                new_room=Room.objects.create(label=label)

        for USER in S:
            new_room.users.add(USER)

        return HttpResponseRedirect(reverse('blog:index'))


@login_required
def ENTER(request, label):
    print("enter : ")
    print(label)

    try:
        room=Room.objects.get(label=label)
    except(Room.DoesNotExist):
        print("존재하지 않는 방입니다. 방 목록 페이지에서 클릭하여 접근해주세요.")
        HttpResponseRedirect(reverse('chat:LIST'))
    else:
        L=room.users.all()
        if(request.user not in L):
            print("you are not allowed to enter this room.")
            return HttpResponseRedirect(reverse('blog:index'))

        messages=reversed(room.messages.order_by('-timestamp')[:50])
        return render(request, "chat/room.html", {
            "room":room,
            "messages":messages,
        })


@login_required
def LIST(request):
    context=dict()
    List=Room.objects.filter(users=request.user)
    context["List"]=List
    return render(request, "chat/room_list.html", context)

