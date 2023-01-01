from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    phone = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'{self.phone} - {self.message[:20]}'
