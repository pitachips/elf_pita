from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from accounts.models import UserProfile


class SignupForm1(UserCreationForm):
    is_agree = forms.BooleanField(label='약관동의', error_messages= { 'requried': '약관동의를 해주셔야 가입이 됩니다.'})


    class Meta(UserCreationForm.Meta):
        # fields = ('username', 'email', )
        fields = UserCreationForm.Meta.fields + ('email', )


    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if email:
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('중복된 이메일')
        return email


class SignupForm2(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('photo', 'intro', 'area', 'sub_area', 'interest', )


class LoginForm(AuthenticationForm):
    pass
