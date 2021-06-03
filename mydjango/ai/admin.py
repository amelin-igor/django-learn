from django.contrib import admin

# Register your models here.

from .models import Metering, Note, Customer, Customerrec, my_control

admin.site.register(Metering)
admin.site.register(Note)
admin.site.register(Customer)
admin.site.register(Customerrec)
admin.site.register(my_control)
