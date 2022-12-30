from django.db import models


class ProductManger(models.Manager):
    def published_articles(self):
        return self.filter(status=True)
