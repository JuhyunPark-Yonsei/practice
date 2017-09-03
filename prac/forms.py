from django import forms
from .models import Post, GameUser

#       validator는 T/F를 return 하는 것이 아니라 error를 raise하는 것으로 데이터 무결성을 검증한다.
'''
#       validator는 보통 model 정의할 때 같이 만드는게 정석이다.
def min_length_3_validator(value):
    if(len(value)<3):
        raise forms.ValidationError("3글자 이상 입력해주세요.")

#       일반폼 만들기 코드 : forms의 Form을 상속해서 만든다.
class PostForm(forms.Form):
    title=forms.CharField(validators=[min_length_3_validator])
    content=forms.CharField(widget=forms.Textarea)
'''

#       이번엔 일반폼이 아니라 모델폼을 만들어보겠다. : forms의 ModelForm을 상속해서 만든다.
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        #   fields="__all__"
        #   위 처럼 fields 항목을 all로 하는 것 보다 list로 하나하나 지정하는것이 정석이다.
        #   fields에서 지정한 항목만 rendering 된다. 따라서 ip, 생성시각, 갱신시각등은 사용자가 입력할 수 없게된다.
        fields=["title", "content", "user_agent"]
        widgets={"user_agent":forms.HiddenInput}


    '''     save함수가 호출되는 시점 : bounded된 폼 객체가 유효성 검사(is_valid())를 통과했을 때(참을 반환했을 때)
    '''
    def save(self, commit=True):
        self.instance=Post(**self.cleaned_data)
        if(commit):         #   commit이 T일때 비로소 DB에 record를 저장하게 된다.
            self.instance.save()

        return self.instance

class GameUserSignupForm(forms.ModelForm):
    class Meta:
        model=GameUser
        fields=["server_name", "username"]

    #   폼 유효성 검사.
    def clean_username(self):
        #   username 필드값의 좌/우 공백을 제거했을 때, 최소 3글자 이상 입력되었는지 체크한다.
        username=self.cleaned_data.get("username", "").strip()
        if(username):
            if(len(username) < 3):
                raise forms.ValidationError("3글자 이상 입력해주세요.")
            #       이 return 값으로 self.cleaned_data["username"] 값이 변경된다.
            #       좌/우 공백이 제거된 username으로 변경된다.
            return username

        raise forms.ValidationError("3글자 이상 입력해주세요.")

    ''' prac/models.py 파일에서 GameUser model 정의할 때 Meta클래스에 unique_together 속성을 사용했기 때문에 
    코드가 매우 짧아졌다. 만약 unique_together를 몰랐다면 아래와 같이 유효성검사를 해주어야 한다.'''
    '''
    def clean(self):
        cleaned_data=super().clean()
        if(self.check_exist(cleaned_data["server_name"], cleaned_data["username"])):
            raise forms.ValidationError("서버에 이미 등록된 이름입니다.")
        return cleaned_data
    
    def check_exist(self, s, u):
        return GameUser.objects.filter(server_name=s, username=u).exists()
    '''

