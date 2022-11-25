from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, username, password=None):


        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone=phone,
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password=None):

        user = self.create_user(
            phone,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
