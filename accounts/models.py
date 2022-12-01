from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.html import format_html

from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    email = models.EmailField(
        verbose_name='ایمیل',
        max_length=255,
        null=True, blank=True,
        unique=True,
    )
    full_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='نام کامل')
    profile_image = models.ImageField(null=True, blank=True, upload_to='user_profile_image', verbose_name='عکس پروفایل')
    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال')
    is_admin = models.BooleanField(default=False, verbose_name='کارمند')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):

        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):

        return self.is_admin

    def showImage(self):
        if self.profile_image:
            return format_html(f'<img src="{self.profile_image.url}" alt="" width="50px" height="50px">')
        else:
            return format_html('پروفایل ندارد')

    showImage.short_description = 'عکس پروفایل'



class OTPCode(models.Model):
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
