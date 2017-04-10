from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.forms import CustomerForm, ModeratorForm, MerchantForm, ProductReviewForm, LoginForm
from store.models import Product, Product_Review
from django.db import connection


def storefront(request):
    try: 
        print(request.session['loggedIn'])
        print(request.session['userName'])
        print(request.session['userType'])
    except KeyError:
        print("No session info")
    watchList = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT p.ID, p.Image, p.Name, p.Seller_Email_id, p.Price, AVG(r.Rating), COUNT(r.id) FROM store_product p LEFT JOIN store_product_review r ON p.ID = r.Product_ID_id GROUP BY p.ID')
        resultSet = cursor.fetchall()
        for row in resultSet:
            watchList.append({'ID': row[0],
                              'Image': row[1],
                              'Name': row[2],
                              'Seller_Email': row[3],
                              'Price': row[4],
                              'Rating': row[5],
                              'NumReviews': row[6]})
    return render(request, 'store/storefront.html',
                  {'watches': watchList})


def logInSignUpChoice(request, logInSignUp):
    return render(request, 'store/logInSignupChoice.html', context={'loginSignup': logInSignUp})


def logout(request):
    request.session['loggedIn'] = False
    request.session['username'] = None
    request.session['userType'] = None
    return redirect('store_front')


def login(request, userType):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST, request.FILES)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            sql = "SELECT Password FROM store_%s WHERE Email = '%s'" % (userType, username)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                pw = cursor.fetchone()
                if pw and pw[0] == password:
                    request.session['loggedIn'] = True
                    request.session['userType'] = userType
                    request.session['userName'] = username
                    return redirect('store_front')
    else:
        loginForm = LoginForm()
    return render(request, 'store/login.html', {'loginForm': loginForm, 'userType': userType})


def signup(request, userType):
    if userType == 'customer':
        FormType = CustomerForm
    elif userType == 'moderator':
        FormType = ModeratorForm
    else:
        FormType = MerchantForm
    if request.method == 'POST':
        signupForm = FormType(request.POST, request.FILES)
        if signupForm.is_valid():
            signupForm.save()
            return redirect('store_front')
    else:
        signupForm = FormType()
        return render(request, 'store/signup.html', {'signupForm': signupForm, 'userType': userType})


def product(request, productID):
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.Product_ID = Product.objects.get(pk = productID)
            review.save()
            return redirect('product_page', productID=productID)
    else:
        form = ProductReviewForm()
        theProduct = Product.objects.raw("SELECT * FROM store_product WHERE ID = %s", [productID])[0]
        productReviews = Product_Review.objects.raw("SELECT * FROM store_product_review WHERE Product_ID_id = %s ORDER BY id DESC", [productID])
        with connection.cursor() as cursor:
            cursor.execute("SELECT AVG(Rating), COUNT(id) FROM store_product_review WHERE Product_ID_id = %s", [productID])
            reviewStats = cursor.fetchone()
        return render(request, 'store/productPage.html', {'product': theProduct,
                                                          'avgRating': reviewStats[0],
                                                          'reviewCount': reviewStats[1],
                                                          'reviews': productReviews,
                                                          'reviewForm': form})


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
