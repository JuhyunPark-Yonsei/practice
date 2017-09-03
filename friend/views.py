from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import FriendShip
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

# Create your views here.
@login_required
def ADD(request):
    context=dict()
    if(request.method == "POST"):
        try:
            ID=request.POST["ID"]
            U=get_user_model().objects.filter(username=ID)
            U=U[0]
        except(KeyError):
            context["error_msg"]="그런 유저가 없습니다. 다시 입력해주세요."
        else:
            context["obj"]=U
    else:
        context["comment"]="ID를 입력해주세요."

    return render(request, "friend/friend_add.html", context)


@login_required
def LIST(request):
    U=get_object_or_404(get_user_model(), username=request.user.username)
    L=[friendship.to_friend for friendship in U.friend_set.all()]

    context=dict()
    context["List"]=L
    return render(request, "friend/friend_list.html", context)


@login_required
def NEW(request):
    try:
        U1=request.user
        U2=get_user_model().objects.filter(id=request.POST["choice"])
        U2=U2[0]
    except(KeyError):
        return render(request, "friend/friend_add.html", {
            "comment":"ID를 입력해주세요."
        })
    else:

        try:
            FriendShip.objects.create(from_friend=U1, to_friend=U2)
            FriendShip.objects.create(from_friend=U2, to_friend=U1)
            return HttpResponseRedirect(reverse_lazy('friend:add'))
        except(IntegrityError):
            return render(request, "friend/friend_add.html", {
                "error_msg": "당신은 이미 이 사람과 친구입니다."
            })

