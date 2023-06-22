from django.db import models

# Create your models here.


class Integrations(models.Model):

    NAME_CLASS = (
        ('iiko', 'iiko'),
    )
    name = models.CharField(max_length=50, choices=NAME_CLASS)

    api_key = models.CharField(max_length=50)
    webhook_uri = models.CharField(max_length=50)
    webhook_token = models.CharField(max_length=64)
    