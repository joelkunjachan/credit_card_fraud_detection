from django.db import models

class registerr(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)

class staff(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    department=models.CharField(max_length=150, default='Fraud Review')

class uploads(models.Model):
    u_id=models.CharField(max_length=150)
    data=models.TextField()
    result=models.CharField(max_length=150)
    status=models.CharField(max_length=150, default='pending')  # pending, approved, blocked
    staff_review=models.TextField(blank=True, null=True)
    reviewed_by=models.CharField(max_length=150, blank=True, null=True)
    reviewed_at=models.DateTimeField(blank=True, null=True)