from django.db import models
from django.contrib.auth.models import User


class Tender(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PUBLISHED', 'Published'),
        ('CLOSED', 'Closed'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='CREATED')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bid(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PUBLISHED', 'Published'),
        ('CANCELED', 'Canceled'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='CREATED')
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} on {self.bid}"


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'employee'
        managed = False


class Organization(models.Model):
    ORGANIZATION_TYPES = [
        ('IE', 'Individual Entrepreneur'),
        ('LLC', 'Limited Liability Company'),
        ('JSC', 'Joint Stock Company')
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=3, choices=ORGANIZATION_TYPES)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'organization'
        managed = False
