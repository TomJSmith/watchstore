from django.shortcuts import render
from django.http import HttpResponse


def storefront(request):
    return render(request, 'store/storefront.html')


def product(request, productName):
    response = "You are looking at the product page for %s" % productName
    return HttpResponse(response)


def user(request, userName):
    response = "user page for user %s" % userName
    return HttpResponse(response)
