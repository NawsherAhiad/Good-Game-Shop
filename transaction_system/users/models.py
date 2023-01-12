from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# model for propile view
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tk = models.IntegerField(default=1500)
    point = models.IntegerField(default=0)

    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.IntegerField()
    buy_point = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

