from email.policy import default
from operator import mod
from statistics import mode
from time import timezone
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import RequestAborted
from django.utils.timezone import now as timezone_now

User = get_user_model()

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_time = models.DateTimeField(default=timezone_now)
    token = models.UUIDField(default=uuid4, editable=False)

    def __str__(self):
        return str(self.token)

    def save(self, *args, **kwargs):
        count = DeviceToken.objects.filter(user=self.user).count()
        if self.user.permission_level == 0 or count == self.user.permission_level:
            raise RequestAborted
        super(DeviceToken, self).save(*args, **kwargs)
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid4, editable=False)
    device_token = models.OneToOneField(DeviceToken, on_delete=models.PROTECT, null=True)
    rose_permission = models.BooleanField(default=False)
    able_to_raise_permission = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - order"
    
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if self.able_to_raise_permission and not self.rose_permission:
            user = self.user
            user.permission_level += 1
            user.save()
    
    def create_device(self):
        device =  DeviceToken.objects.create(user=self.user)
        self.device_token = device
        self.save()
        return device
         
