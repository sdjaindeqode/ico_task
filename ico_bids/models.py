from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Token(models.Model):
    name = models.CharField(max_length=30)
    available_token = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name
    

class Bid(models.Model):
    STATUS = (
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    number_of_token = models.IntegerField(validators=[MinValueValidator(1)])
    bid_price = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alloted_tokens = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=STATUS, default='PENDING'
    )