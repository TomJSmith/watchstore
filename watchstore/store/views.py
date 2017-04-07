from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.forms import CustomerForm, ModeratorForm, MerchantForm


def storefront(request):
    return render(request, 'store/storefront.html')


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


def product(request, productName):
    response = "You are looking at the product page for %s" % productName
    return HttpResponse(response)


def user(request, userName):
    response = "user page for user %s" % userName
    return HttpResponse(response)
