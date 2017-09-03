from django import forms
from .models import Post


#       일반 폼 클래스가 아닌 모델 폼 클래스를 만든다.
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields="__all__"
