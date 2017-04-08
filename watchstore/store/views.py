from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.forms import CustomerForm, ModeratorForm, MerchantForm, ProductReviewForm
from store.models import Product
from itertools import chain


def storefront(request):
    watches = Product.objects.raw('SELECT * FROM store_product ORDER BY name')
    return render(request, 'store/storefront.html',
                  {'watches': watches, }
                  )


def logInSignUpChoice(request, logInSignUp):
    return render(request, 'store/logInSignupChoice.html', context={'loginSignup': logInSignUp})


def login(request, userType):
    loginForm = None
    if request.method == 'POST':
        loginForm = CustomerForm(request.POST, request.FILES)
        if loginForm.is_valid():
            loginForm.save()
            return redirect('store_front')
    else:
        loginForm = CustomerForm()
    return render(request, 'store/login.html', {'loginForm': loginForm})


def signup(request, userType):
    if userType == 'customer':
        FormType = CustomerForm
    elif userType == 'moderator':
        FormType = ModeratorForm
    else:
        FormType = MerchantForm
    signupForm = None
    if request.method == 'POST':
        signupForm = FormType(request.POST, request.FILES)
        if signupForm.is_valid():
            signupForm.save()
            return redirect('store_front')
    else:
        signupForm = FormType()
    return render(request, 'store/signup.html', {'signupForm': signupForm, 'userType': userType})


def product(request, productID):
    form = ProductReviewForm()
    theProduct = Product.objects.raw("SELECT * FROM store_product WHERE ID = %s", [productID])[0]
    response = "You are looking at the product page for %s" % productID
    return render(request, 'store/productPage.html', {'product': theProduct, 'reviewForm': form})


def merchant(request, merchantID):
    print(merchantID)
    return HttpResponse("merchant page for merchant " + merchantID)


def user(request, userName):
    response = "user page for user %s" % userName
    return HttpResponse(response)


def search(request):
    return render(request, 'store/searchform.html')


def results(request):
    if request.method == "POST":
        query = request.POST["query"]
        try:
            p1 = Product.objects.filter(Name__icontains=query)
            p2 = Product.objects.filter(Description__icontains=query)
            p3 = Product.objects.filter(Brand__icontains=query)
            p4 = Product.objects.filter(Type__icontains=query)
            p5 = Product.objects.filter(Compatibility__icontains=query)
            products = p1 | p2 | p3 | p4 | p5
            return render(request, 'store/results.html',
                          {'products': products, 'query': query, }
                          )
        except Product.DoesNotExist:
            return HttpResponse("No search results")
    else:
        return redirect('store_front')
