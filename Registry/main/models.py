from django.db import models


class StatusServiceENUM(models.TextChoices):
    active = 'active', 'Active'
    inactive = 'inactive', 'Inactive'
    error = 'error', 'Error'
    pending = 'pending', 'Pending'
    waiting = 'waiting', 'Waiting'


class Service(models.Model):
    service_name = models.CharField(max_length=255)
    status = models.CharField(choices=StatusServiceENUM.choices, default=StatusServiceENUM.active, max_length=20)
    description = models.TextField()
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(null=True)


class Version(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    version_number = models.IntegerField(default=1)
    release_date = models.DateField(auto_now=True)
    service_url = models.URLField(max_length=255)

