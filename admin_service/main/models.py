from django.db import models


class Admin(models.Model):
    first_name = models.TextField(max_length=255, blank=False, null=False)
    last_name = models.TextField(max_length=255, blank=False, null=False)
    username = models.TextField(unique=True, blank=False, null=False)
    password = models.TextField(max_length=255, blank=False, null=False)
    email = models.TextField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)


class Performance(models.Model):
    user_id = models.IntegerField(null=False, blank=False)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=False)
    report = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    recommendation = models.TextField(null=False, blank=False)


