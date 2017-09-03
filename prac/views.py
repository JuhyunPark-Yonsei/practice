from django.shortcuts import render, redirect, get_object_or_404
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .forms import PostForm
from .models import Post
# Create your views here.


#   function based view 연습.
def post_new(request):
    if(request.method == "POST"):
        form=PostForm(request.POST, request.FILES)      #       폼 객체(form)은 bound 상태가 된다.
        if form.is_valid():                             #       bound 이후에 유효성 검사까지 통과했음.
            #       방법 1)
            post=Post()                                 #       이제 DB에 저장하기 위한 database table record(instance)를 만든다.
            post.title=form.cleaned_data["title"]       #       record instance에 값을 채워넣는다.
            post.content=form.cleaned_data["content"]   #       record instance에 값을 채워넣는다.
            post.save()                                 #       DB에 저장한다.

            #       방법 2)
            '''
            post=Post(title=form.cleaned_data["title"],
                        content=form.cleaned_data["content"])
            post.save()
            '''

            #       방법 3)
            '''
            post = Post.objects.create(title=form.cleaned_data["title"],
                                       content=form.cleaned_data["content"])
            '''

            #       방법 4)
            #   post=Post.objects.create(**form.cleaned_data)


            #       방법 5)
            #   post=form.save(commit=False)
            #   post.ip=request.META["REMOTE_ADDR"]
            #   post.save()         #       post.save(commit=True)랑 똑같은 문장이다.


            #       객체로부터 값 전달받으면 무결성 검사하고 view에서 적당한 로직을 처리한 뒤에 주로 redirect 하는게 정석.
            return redirect("/prac/")
    else:
        form=PostForm()         #   인자없이 폼 객체(forms)를 만들면 Unbounded 상태이다.

    context=dict()
    context["form"]=form
    return render(request, "prac/post_form.html", context)


def post_edit(request, id):
    post=get_object_or_404(Post, id=id)

    if(request.method == "POST"):
        form=PostForm(request.POST, request.FILES, instance=post)
        if(form.is_valid()):
            post=form.save(commit=False)

            #       ip 속성은 form 클래스 만들 때 fields 속성에 포함되어 있지 않았기 때문에 내가 직접 하드코딩한다.
            post.ip=request.META["REMOTE_ADDR"]
            post.save()
            return redirect("/prac/")
    else:
        form=PostForm(instance=post)

    return render(request, "prac/post_form.html", {"form" : form})


def post_list(request):
    return HttpResponse()


def post_list1(request):
    title="채팅앱"
    return HttpResponse('''
        <h1>Web App</h1>
        <p>real time 실시간 {var}을 만드는 것이 목표입니다.</p>
        '''.format(var=title))


def post_list2(request):
    context=dict()
    context["title"]="채팅앱"
    return render(request, "prac/post_list.html", context)


def post_list3(request):
    return JsonResponse({
        "msg" : "Django Framework",
        "items" : ["chat", "web socket", "channels", "blog"],
    }, json_dumps_params={"ensure_ascii":False})


def excel_download(request):
    filepath=os.path.join(settings.BASE_DIR, 'SampleXLSFile_19kb.xls')
    filename=os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        response=HttpResponse(f, content_type="application/vnd.ms-excel")
        response["Content-Disposition"]="attachment"
        filename="{}".format(filename)
        return response
