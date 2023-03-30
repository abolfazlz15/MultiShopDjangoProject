from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, email, full_name, password=None):


        if not phone:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone=phone,
            email=email,
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, email,  password=None):

        user = self.create_user(
            phone,
            email=email,
            full_name=full_name,
            password=password,

        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
