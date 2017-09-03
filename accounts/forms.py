from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Profile


class SignupForm(UserCreationForm):
    phone_number=forms.CharField()
    address=forms.CharField()

    class Meta(UserCreationForm.Meta):
        fields=UserCreationForm.Meta.fields + ("email", )

    def save(self):
        user=super().save()
        profile=Profile.objects.create(
            user=user,  phone_number=self.cleaned_data["phone_number"],
            address=self.cleaned_data["address"]
        )
        return user


class LoginForm(AuthenticationForm):
    answer=forms.IntegerField(label="3 + 3 = ?")

    #       form field 데이터 유효성 검사.
    def clean_answer(self):
        answer=self.cleaned_data.get("answer", None)
        if(answer!=6):
            raise forms.ValidationError("틀렸습니다. 로그인할 수 없습니다.")
        return answer
