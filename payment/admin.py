from django.contrib import admin
from .models import ShippingAddress, Order,OrderItem
from django.contrib.auth.models import User

#Register the model on the admin section
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Create an orderItem inline
class OrderItemInline(admin.StackedInline):
  model =OrderItem
  extra = 0
  

class OrderAdmin(admin.ModelAdmin):
  model = Order
  readonly_fields = ["date_ordered"]
  field = ["user","full_name","email","shipping_address","amount_paid","date_ordered","shipped","date_shipped"]
  inlines = [OrderItemInline]

#unregister order model
admin.site.unregister(Order)

#re register
admin.site.register(Order, OrderAdmin)



# Register your models here.

