from django.forms import ModelForm
from store.models import Customer, Moderator, Merchant, Product_Review


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['Email', 'Password', 'FName', 'LName', 'Address']


class ModeratorForm(ModelForm):
    class Meta:
        model = Moderator
        fields = ['Email', 'Password', 'FName', 'LName', 'Resp_Level']


class MerchantForm(ModelForm):
    class Meta:
        model = Merchant
        fields = ['Email', 'Password', 'FName', 'LName', 'Banking_Info', 'Address']


class ProductReviewForm(ModelForm):
    class Meta:
        model = Product_Review
        fields = ['Feedback', 'Customer_Email', 'Rating']
