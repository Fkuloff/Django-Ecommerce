from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    # username = models.CharField(max_length=64, unique=True, blank=True)

    email = models.EmailField(max_length=64, unique=True)
    phone_number = models.CharField(max_length=12, unique=True)

    profile_avatar = models.ImageField(blank=True, upload_to='userprofile', default='userprofile/img_avatar.png')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = AccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

# class UserProfile(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#
#     address_line_1 = models.CharField(max_length=50, blank=True)
#     address_line_2 = models.CharField(max_length=50, blank=True)
#
#     profile_avatar = models.ImageField(blank=True, upload_to='userprofile',
#                                        default='userprofile/img_avatar.png')
#
#     country = models.CharField(max_length=50, blank=True)
#     state = models.CharField(max_length=50, blank=True)
#     city = models.CharField(max_length=50, blank=True)
#
#     def __str__(self):
#         return self.user.first_name
#
#     def full_address(self):
#         return f'{self.address_line_1} {self.address_line_2}'
