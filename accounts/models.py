from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.html import format_html

from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    phone = models.CharField(max_length=11, unique=True, verbose_name='phone number')
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        null=True, blank=True,
        unique=True,
    )
    full_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='fullname')
    profile_image = models.ImageField(null=True, blank=True, upload_to='user_profile_image', verbose_name='profile image')
    is_active = models.BooleanField(default=True, verbose_name='avtive user')
    is_admin = models.BooleanField(default=False, verbose_name='staff user')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

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
            return format_html('there is no profile image')

    showImage.short_description = 'there is no profile image'






class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    fullname = models.CharField(max_length=45)
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=11)
    zip_code = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.fullname} - {self.user.phone}'