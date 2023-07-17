from django.db import models


class ProductManger(models.Manager):
    def published(self):
        return self.filter(status=True)
