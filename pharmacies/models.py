from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users.models import AppUser
# Create your models here.

class Manager(models.Model):
    app_user = models.OneToOneField(
        verbose_name = 'App user',
        to = AppUser,
        on_delete = models.CASCADE,
        primary_key = True,
    )

    phone_number = PhoneNumberField(
        verbose_name = 'Phone number',
        blank=True,
    )

    company_name = models.CharField(
        verbose_name = 'Company name',
        max_length = 255,
    )

    created = models.DateTimeField(
        verbose_name = "Created",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Updated",
        auto_now = True,
    )

    class Meta:

        verbose_name = "Manager"
        verbose_name_plural = "Managers"
        ordering = ('-created',)

    def __str__(self):
        return '%s' % self.app_user.email

def _upload_path(instance,filename):
    return instance.get_upload_path(filename)

class Document(models.Model):
    title = models.CharField(
        verbose_name = 'Title',
        max_length = 255,
    )

    document = models.FileField(
        verbose_name = "Document",
        upload_to=_upload_path,
    )

    manager = models.ForeignKey(
        verbose_name = "Manager",
        to = Manager, 
        on_delete = models.CASCADE
    )

    created = models.DateTimeField(
        verbose_name = "Created",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Updated",
        auto_now = True,
    )

    class Meta:

        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ('-created',)

    def __str__(self):
        return "%s" % self.pk

    def get_upload_path(self, filename):
        return 'documents/user_{0}/{1}'.format(self.manager.pk, filename)


class Order(models.Model):
    ORDER_STATUSES = (
        ('Processing', 'В обработке'),
        ('Processed', 'Обработан'),
        ('Canceled', 'Отменён'),
    )

    status = models.CharField(max_length=13, choices=ORDER_STATUSES)

    comment = models.TextField(
        verbose_name = "Comment",
    )

    manager = models.ForeignKey(
        verbose_name = "Manager",
        to = Manager, 
        on_delete = models.CASCADE
    )

    document = models.ForeignKey(
        verbose_name = "Document",
        to = Document, 
        on_delete = models.CASCADE
    )

    created = models.DateTimeField(
        verbose_name = "Created",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Updated",
        auto_now = True,
    )

    class Meta:

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ('-created',)

    def __str__(self):
        return self.pk