from django import forms
from django.contrib.auth import password_validation

from .models import Account


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваше имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваша фамилия',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Телефон',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль',
    }),
        min_length=8,
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_date = super(RegistrationForm, self).clean()
        password = cleaned_date.get('password')
        confirm_password = cleaned_date.get('confirm_password')

        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            raise forms.ValidationError(
                error
            )

        if password != confirm_password:
            raise forms.ValidationError(
                'Пароли не совпадают'
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'


class UserForm(forms.ModelForm):
    profile_avatar = forms.ImageField(required=False,
                                      error_messages={'invalid': {"Image files only"}}, widget=forms.FileInput)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'profile_avatar')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# class UserProfileForm(forms.ModelForm):
#     profile_avatar = forms.ImageField(required=False,
#     error_messages={'invalid': {"Image files only"}}, widget=forms.FileInput)
#     class Meta:
#         model = UserProfile
#         fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_avatar')
#
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
