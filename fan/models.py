from django.db import models

class Fan(models.Model):
    name = models.CharField(max_length=100)
    voltage = models.FloatField(default=220)
    power_factor = models.FloatField(default=0.8)

class FanLog(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    speed_level = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
