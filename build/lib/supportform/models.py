from django.db import models
from django.contrib.auth.models import User

class Support(models.Model):
    email = models.EmailField(blank=True,null=True)
    subject = models.CharField(max_length=500)
    description = models.TextField()

    @property
    def user(self):
        try:
            return User.objects.get(email=self.email)
        except User.DoesNotExists:pass
