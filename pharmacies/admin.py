from django.contrib import admin
from .models import (
    Document,
    Order,
    Manager
)
# Register your models here.
admin.site.register(Document)
admin.site.register(Order)
admin.site.register(Manager)