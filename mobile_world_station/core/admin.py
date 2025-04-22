from django.contrib import admin

import core.models as models
# Register your models here.

admin.site.register(models.Item)
admin.site.register(models.ContactUsEmail)
admin.site.register(models.AppointmentEmail)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)