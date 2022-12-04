from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True, unique=True)
    use_sms = models.BooleanField(default=True)
    
    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())


    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False



