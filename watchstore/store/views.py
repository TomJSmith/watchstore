from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.forms import CustomerForm, ModeratorForm, MerchantForm, ProductReviewForm, MerchantReviewForm, LoginForm, \
    AddToCart, ProductForm, OrderForm, CreditForm
from store.models import Product, Product_Review, Merchant_Review, Customer, Cart, Merchant, Order, Credit_Card
from django.db import connection


def storefront(request):
    if 'userName' not in request.session:
        request.session['userName'] = None
    if 'loggedIn' not in request.session:
        request.session['loggedIn'] = False

    watchList = []
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT p.ID, p.Image, p.Name, p.Seller_Email_id, p.Price, AVG(r.Rating), COUNT(r.id) FROM store_product p LEFT JOIN store_product_review r ON p.ID = r.Product_ID_id GROUP BY p.ID')
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
            if userType == "customer":
                Cart.objects.create(Customer_Email=Customer.objects.get(pk=signupForm.cleaned_data['Email']))
            return redirect('store_front')
    else:
        signupForm = FormType()
        return render(request, 'store/signup.html', {'signupForm': signupForm, 'userType': userType})


def product(request, productID):
    with connection.cursor() as cursor:
        cartID = ''
        if request.session['userName']:
            cursor.execute("SELECT id FROM store_cart WHERE Customer_Email_id=%s",
                           [request.session['userName']])
            cartID = cursor.fetchone()[0]
    if request.method == 'POST':
        if 'cartButton' in request.POST:
            form = AddToCart(request.POST, request.FILES)
            if form.is_valid():
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO store_cart_Product_ID (cart_id, product_id) VALUES (%s, %s)",
                                   [cartID, productID])
                return redirect('store_front')
            print(form.errors)

        elif 'reviewButton' in request.POST:
            print('reviewButton')
            form = ProductReviewForm(request.POST, request.FILES)
            if form.is_valid():
                review = form.save(commit=False)
                review.Product_ID = Product.objects.get(pk=productID)
                review.Customer_Email = Customer.objects.get(pk=request.session['userName'])
                review.save()
                return redirect('product_page', productID=productID)
    else:
        form = ProductReviewForm()
        theProduct = Product.objects.raw("SELECT * FROM store_product WHERE ID = %s", [productID])[0]
        productReviews = Product_Review.objects.raw(
            "SELECT * FROM store_product_review WHERE Product_ID_id = %s ORDER BY id DESC", [productID])
        with connection.cursor() as cursor:
            cursor.execute("SELECT AVG(Rating), COUNT(id) FROM store_product_review WHERE Product_ID_id = %s",
                           [productID])
            reviewStats = cursor.fetchone()
            cursor.execute("SELECT COUNT(*) FROM store_cart_Product_ID WHERE cart_id=%s AND product_id=%s", [cartID, productID])
            inCart = False
            if cursor.fetchone()[0] > 0:
                inCart = True
        return render(request, 'store/productPage.html', {'product': theProduct,
                                                          'avgRating': reviewStats[0],
                                                          'reviewCount': reviewStats[1],
                                                          'reviews': productReviews,
                                                          'reviewForm': form,
                                                          'inCart': inCart})


def merchant(request, merchantID):
    if request.method == 'POST':
        form = MerchantReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.Merchant_Email = Merchant.objects.get(pk=merchantID)
            review.Customer_Email = Customer.objects.get(pk=request.session['userName'])
            review.save()
            return redirect('merchant_page', merchantID=merchantID)
    else:
        productList = []
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT * FROM (SELECT p.ID, p.Image, p.Name, p.Seller_Email_id, p.Brand, p.Price, AVG(r.Rating), COUNT(r.id) FROM store_product p LEFT JOIN store_product_review r ON p.ID = r.Product_ID_id GROUP BY p.ID) WHERE Seller_Email_id = %s',
                [merchantID])
            resultSet = cursor.fetchall()
            for row in resultSet:
                productList.append({'ID': row[0],
                                    'Image': row[1],
                                    'Name': row[2],
                                    'Seller_Email': row[3],
                                    'Brand': row[4],
                                    'Price': row[5],
                                    'Rating': row[6],
                                    'NumReviews': row[7]})
                #        products = Product.objects.raw("SELECT * FROM store_product WHERE Seller_Email_id = %s", [merchantID])
        reviews = Merchant_Review.objects.raw(
            "SELECT * FROM store_merchant_review WHERE Merchant_Email_id = %s ORDER BY id DESC", [merchantID])
        merchant = Merchant.objects.raw("SELECT * FROM store_merchant WHERE EMAIL = %s", [merchantID])[0]
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(id), AVG(Rating) FROM store_merchant_review WHERE Merchant_Email_id = %s",
                           [merchantID])
            reviewStats = cursor.fetchone()
        form = MerchantReviewForm()
        return render(request, 'store/merchantPage.html', {'merchant': merchant,
                                                           'reviewCount': reviewStats[0],
                                                           'avgRating': reviewStats[1],
                                                           'products': productList,
                                                           'reviews': reviews,
                                                           'reviewForm': form})


def user(request, userName):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            if request.POST['areFriends'] == "false":
                cursor.execute("INSERT INTO store_friends (Friend_1_id, Friend_2_id) VALUES (%s, %s)",
                               [request.session['userName'], userName])
            else:
                cursor.execute("DELETE FROM store_friends WHERE Friend_1_id=%s AND Friend_2_id=%s",
                               [request.session['userName'], userName])
        return redirect('user_profile', userName)
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM store_friends WHERE Friend_1_id=%s AND Friend_2_id=%s",
                           [request.session['userName'], userName])
            areFriends = False
            if cursor.fetchone()[0] == 1:
                areFriends = True
            cursor.execute("SELECT FName, LName, Email FROM store_customer WHERE Email = %s", [userName])
            theCustomer = cursor.fetchone()
            cursor.execute(
                "SELECT Friend_2_id, FName, LName FROM store_friends, store_customer WHERE Friend_2_id=Email AND Friend_1_id=%s",
                [userName])
            friends = cursor.fetchall()
        return render(request, 'store/customerPage.html', {'customer': theCustomer,
                                                           'areFriends': areFriends,
                                                           'friendsList': friends})


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


def myCustomerAccount(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            prodID = int(request.POST['prodID'])
            myCart = Cart.objects.get(Customer_Email=Customer.objects.get(pk=request.session['userName']))
            myCart.Product_ID.remove(prodID)
            myCart.save()
            return redirect('my_account')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM store_customer WHERE Email = %s", [request.session['userName']])
            customer = cursor.fetchone()
            cursor.execute(
                "SELECT Friend_2_id, FName, LName FROM store_friends, store_customer WHERE Friend_2_id=Email AND Friend_1_id=%s",
                [request.session['userName']])
            friends = cursor.fetchall()
        cart = Cart.objects.get(Customer_Email=Customer.objects.get(pk=request.session['userName'])).Product_ID.all()
        orders = Order.objects.filter(Placed_By=Customer.objects.get(pk=request.session['userName']))  # .Order_Number.all()
        return render(request, 'store/myCustomerAccount.html', {'email': customer[0],
                                                                'fName': customer[2],
                                                                'lName': customer[3],
                                                                'address': customer[4],
                                                                'cart': cart,
                                                                'orders': orders,
                                                                'friendsList': friends})


def myModeratorAccount(request):
    if request.method == 'POST':
        theMerchant = request.POST['merchant_email']
        if request.POST['decision'] == 'approve':
            approval = 'APP'
        else:
            approval = 'RJ'
        with connection.cursor() as cursor:
            cursor.execute("UPDATE store_merchant SET Status = %s, Reviewed_By_id = %s WHERE Email = %s",
                           [approval, request.session['userName'], theMerchant])
        return redirect('my_account')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT Email, FName, LName, Resp_Level FROM store_moderator WHERE Email = %s",
                           [request.session['userName']])
            theMod = cursor.fetchone()
            cursor.execute("SELECT Email, FName, LName, Banking_Info, Address FROM store_merchant WHERE Status='PD'")
            pendingMerchants = cursor.fetchall()
        return render(request, 'store/myModeratorAccount.html', {'email': theMod[0],
                                                                 'fName': theMod[1],
                                                                 'lName': theMod[2],
                                                                 'responsibility': theMod[3],
                                                                 'pendingMerchants': pendingMerchants})


def myMerchantAccount(request):
    if request.method == 'POST':
        newProduct = ProductForm(request.POST, request.FILES)
        if newProduct.is_valid():
            newProduct = newProduct.save(commit=False)
            newProduct.Seller_Email_id = Merchant.objects.get(pk=request.session['userName'])
            newProduct.save()
            return redirect('my_account')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM store_merchant WHERE Email = %s", [request.session['userName']])
            theMerchant = cursor.fetchone()
        prodForm = ProductForm()
        return render(request, 'store/myMerchantAccount.html', {'email': theMerchant[0],
                                                                'fName': theMerchant[2],
                                                                'lName': theMerchant[3],
                                                                'bankingInfo': theMerchant[4],
                                                                'address': theMerchant[5],
                                                                'status': theMerchant[6],
                                                                'form': prodForm})


def myAccount(request):
    if not request.session['loggedIn']:
        return redirect('store_front')
    else:
        userType = request.session['userType']
        if userType == 'customer':
            return myCustomerAccount(request)
        elif userType == 'moderator':
            return myModeratorAccount(request)
        else:
            return myMerchantAccount(request)


def order(request, orderNumber):
    if not request.session['loggedIn']:
        return redirect('store_front')
    else:
        userType = request.session['userType']
        if userType == 'customer':
            anOrder = Order.objects.get(Order_Number=orderNumber)
            if request.session['userName'] != anOrder.Placed_By.Email:
                return redirect('store_front')
            else:
                products = anOrder.Product_ID.all()
                return render(request, 'store/order.html', {'order': anOrder,
                                                            'products': products})
        elif userType == 'moderator':
            return redirect('store_front')
        else:
            return redirect('store_front')


def addCreditCard(request):
    if not request.session['loggedIn']:
        return redirect('store_front')
    else:
        FormType = CreditForm
        if request.method == 'POST':
            creditCardForm = FormType(request.POST, request.FILES)
            if 'add' in request.POST:
                if creditCardForm.is_valid():
                    ccNum = creditCardForm.cleaned_data['Number']
                    exMonth = creditCardForm.cleaned_data['ExpiryMonth']
                    exYear = creditCardForm.cleaned_data['ExpiryYear']
                    lName = creditCardForm.cleaned_data['LName']
                    fName = creditCardForm.cleaned_data['FName']
                    securityCode = creditCardForm.cleaned_data['Security_Code']
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO store_credit_card (Number, FName, LName, ExpiryMonth, ExpiryYear, Security_Code, CEmail_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            [ccNum, fName, lName, exMonth, exYear, securityCode, request.session['userName']])
                    creditCardForm = FormType()
                    creditCards = Credit_Card.objects.filter(
                        CEmail=Customer.objects.get(pk=request.session['userName']))
                    return render(request, 'store/checkout.html',
                                  {'creditCardForm': creditCardForm, 'creditcard': creditCards})
            elif 'select' in request.POST:
                ccNum = request.POST['creditCardSelection']
                print(ccNum)
                request.session['ccNum'] = ccNum
                return redirect('order_finalization')
        creditCardForm = FormType()
        creditCards = Credit_Card.objects.filter(CEmail=Customer.objects.get(pk=request.session['userName']))
        print('render checkout')
        return render(request, 'store/checkout.html', {'creditCardForm': creditCardForm, 'creditcard': creditCards})


def orderInfo(request):
    print(request.POST)
    if not request.session['loggedIn']:
        return redirect('store_front')
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT p.Name, p.Price, p.ID FROM store_product p, store_cart c, store_cart_Product_ID cp WHERE c.Customer_Email_id=%s AND c.id = cp.cart_id AND cp.product_id = p.id",
                [request.session['userName']])
            cartItems = cursor.fetchall()
            cursor.execute(
                "SELECT SUM(p.Price) FROM store_product p, store_cart c, store_cart_Product_ID cp WHERE c.Customer_Email_id=%s AND c.id = cp.cart_id AND cp.product_id = p.id",
                [request.session['userName']])
            totalPrice = cursor.fetchone()[0]
            cursor.execute("SELECT Address FROM store_customer WHERE Email = %s", [request.session['userName']])
            address = cursor.fetchone()[0]
        if request.method == 'POST' and 'placeOrder' in request.POST:
            print('working')
            newOrder = Order()
            newOrder.Total_Price = totalPrice
            newOrder.Shipping_Info = request.POST['shippingAddress']
            newOrder.Billing_Info = request.session['ccNum']
            request.session['ccNum'] = None
            newOrder.Placed_By = Customer.objects.get(pk=request.session['userName'])
            newOrder.save()
            for item in cartItems:
                newOrder.Product_ID.add(item[2])
            myCart = Cart.objects.get(Customer_Email=request.session['userName'])
            myCart.Product_ID.clear()
            return order(request, newOrder.Order_Number)
        return render(request, 'store/orderInfo.html', {'cartItems': cartItems,
                                                        'total': totalPrice,
                                                        'shippingAddress': address,
                                                        'creditCard': request.session['ccNum']})
