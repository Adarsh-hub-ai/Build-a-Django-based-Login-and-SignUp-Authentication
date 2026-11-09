from django.db import models

class SignIn(models.Model):
    name = models.CharField(max_length= 250)
    email = models.EmailField(max_length= 250)

class PendingSignup(models.Model):
    name = models.CharField(max_length= 250)
    email = models.EmailField(max_length= 250, unique= True)
    otp_hash = models.CharField(max_length= 128)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)

    

    



    
