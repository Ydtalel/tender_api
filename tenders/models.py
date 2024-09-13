from django.db import models


class Employee(models.Model):
    """Модель пользователя"""

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        managed = True  # поменять на false перед последним коммитом
        db_table = 'employee'


class Organization(models.Model):
    """Модель организации"""

    ORGANIZATION_TYPES = [
        ('IE', 'IE'),
        ('LLC', 'LLC'),
        ('JSC', 'JSC'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=3, choices=ORGANIZATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True  # поменять на false перед последним коммитом
        db_table = 'organization'


class OrganizationResponsible(models.Model):
    """Модель для связи организации с ответственным пользователем"""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.organization.name}'

    class Meta:
        managed = True  # поменять на false перед последним коммитом
        db_table = 'organization_responsible'


class Tender(models.Model):
    """Модель тендера"""

    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PUBLISHED', 'Published'),
        ('CLOSED', 'Closed'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('Construction', 'Construction'),
        ('Consulting', 'Consulting'),
        ('IT', 'IT'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='CREATED')
    service_type = models.CharField(max_length=50,
                                    choices=SERVICE_TYPE_CHOICES)
    version = models.PositiveIntegerField(default=1)
    creator = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TenderVersion(models.Model):
    """Модель для хранения версий тендера"""
    tender = models.ForeignKey(Tender, related_name='versions',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10)
    service_type = models.CharField(max_length=50)
    version = models.PositiveIntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version} of {self.tender.name}"


class Bid(models.Model):
    """Модель предложения на тендер"""

    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PUBLISHED', 'Published'),
        ('CANCELED', 'Canceled'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='CREATED')
    version = models.PositiveIntegerField(default=1)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    creator = models.ForeignKey(Employee, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BidVersion(models.Model):
    """Модель для хранения версий предложения"""
    bid = models.ForeignKey(Bid, related_name='versions',
                            on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10)
    version = models.PositiveIntegerField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version} of {self.bid.name}"
