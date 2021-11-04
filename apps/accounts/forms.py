from django import forms
from django.contrib.auth import password_validation
from django.core.validators import RegexValidator
from .models import Account


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваше имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ваша фамилия',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'type': 'email',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль', 'type': 'password',
    }),
        min_length=8,
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль', 'type': 'password',
    }), min_length=8,
    )

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Телефон', 'type': 'phone',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number']

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
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# class UserProfileForm(forms.ModelForm):
#     profile_avatar = forms.ImageField(required=False, error_messages={'invalid': {"Image files only"}}, widget=forms.FileInput)
#
#     class Meta:
#         model = UserProfile
#         fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_avatar')
#
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
