from .models import Post
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from django.contrib import messages

# Create your views here.
def post_list(request):
    context=dict()
    qs=Post.objects.all()

    '''   html input 폼으로부터 값을 전달받는다.
       name 속성(key)이 "str"인 input 폼을 찾아서 type 속성에서 명시하는 포맷(text 형태)으로
       전달된 값을 반환받는다. 반환된 값을 변수 q에 저장해둔다.
       만약 input 폼으로부터 전달받는 값이 아무것도 없는 문자열이면 ("") q에는 "Nil"라는 문자열로 저장해둔다.    '''
    q=request.GET.get("str", "Nil")


    if(q!="Nil"):
        qs=qs.filter(title__icontains=q)

    context["post_list"]=qs
    context["q"]=q
    context["search"]="제목을 입력해주세요."
    return render(request, 'blog/post_list.html', context)


def post_detail(request, id):
    #   try:
    #       post=Post.objects.get(id=id)
    #   except Post.DoesNotExist:
    #       raise Http404

    context=dict()
    post=get_object_or_404(Post, id=id)
    context["post"]=post
    return render(request, "blog/post_detail.html", context)


def post_new(request):
    if(request.method == "POST"):
        form=PostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save()
            messages.success(request, "새 포스팅을 저장했습니다.")
            return redirect(post)       #   post 모델(클래스)에 정의되어 있는 get_absolute_url() 함수가 호출된다.
                                        #   즉, redirect(post.get_absolute_url())
    else:
        form=PostForm()

    return render(request, "blog/post_form.html", {"form":form})


def post_edit(request, id):
    post=get_object_or_404(Post, id=id)

    if(request.method == "POST"):
        form=PostForm(request.POST, request.FILES, instance=post)
        if(form.is_valid()):
            post=form.save()
            messages.success(request, "포스팅을 수정했습니다.")
            return redirect(post)
    else:
        form=PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form":form})


class MyDetailView(object):
    def __init__(self, model):
        self.model=model

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, id=kwargs["id"])


    def get_template_name(self):
        return "{}/{}_detail.html".format(self.model._meta.app_label, self.model._meta.model_name)

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.get_template_name(), {
            self.model._meta.model_name : self.get_object(*args, **kwargs)
        })

    @classmethod
    def as_view(cls, model):
        def view(request, *args, **kwargs):
            self=cls(model)
            return self.dispatch(request, *args, **kwargs)
        return view

