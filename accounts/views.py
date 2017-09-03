from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm


# Create your views here.
@login_required
def profile(request):
    context=dict()
    return render(request, "accounts/profile.html", context)


def signup(request):
    if request.method == "POST":
        form=SignupForm(request.POST)
        if(form.is_valid()):
            user=form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form=SignupForm()

    context=dict()
    context["form"]=form
    return render(request, "accounts/signup_form.html", context)