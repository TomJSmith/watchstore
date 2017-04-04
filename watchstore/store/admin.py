from django.contrib import admin

# Register your models here.
from .models import Customer
from .models import Credit_Card
from .models import Moderator
from .models import Merchant
from .models import Product
from .models import Order
from .models import Merchant_Review
from .models import Product_Review
from .models import Cart
from .models import Friends
from .models import ProductImage

admin.site.register(Customer)
admin.site.register(Credit_Card)
admin.site.register(Moderator)
admin.site.register(Merchant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Merchant_Review)
admin.site.register(Product_Review)
admin.site.register(Cart)
admin.site.register(Friends)
admin.site.register(ProductImage)