from django.forms import ModelForm
from django import forms
from store.models import Customer, Moderator, Merchant, Product_Review, Cart, Product


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", max_length=100)


class AddToCart(ModelForm):
    class Meta:
        model = Cart
        fields = []


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
        fields = ['Feedback', 'Rating']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['Name', 'Description', 'Price', 'Brand', 'Type', 'Compatibility', 'Image']
