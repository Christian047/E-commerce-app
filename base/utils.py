import json
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.exceptions import ObjectDoesNotExist

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_profile = request.user.userprofile

    if user_profile.wallet_balance >= product.price:
        
        # Update the user's wallet balance
        user_profile.wallet_balance -= product.price
        user_profile.save()

        # Add the product to the cart (You should have a cart model for this)
        # ...

        return render(request, 'cart/success.html', {'product': product})
    else:
        return render(request, 'cart/insufficient_funds.html', {'product': product})


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            if cart[i]['quantity'] > 0:
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'imageURL': product.imageURL}, 'quantity': cart[i]['quantity'],
                    'digital': product.digital, 'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    cartItems = 0
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    items = []

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:
            customer = Customer.objects.create(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),
        )

    return customer, order



# import json
# from .models import *
# from django.core.exceptions import ObjectDoesNotExist

# def cookieCart(request):

# 	#Create empty cart for now for non-logged in user
# 	try:
# 		cart = json.loads(request.COOKIES['cart'])
# 	except:
# 		cart = {}
# 		print('CART:', cart)

# 	items = []
# 	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
# 	cartItems = order['get_cart_items']

# 	for i in cart:
# 		#We use try block to prevent items in cart that may have been removed from causing error
# 		try:	
# 			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
# 				cartItems += cart[i]['quantity']

# 				product = Product.objects.get(id=i)
# 				total = (product.price * cart[i]['quantity'])

# 				order['get_cart_total'] += total
# 				order['get_cart_items'] += cart[i]['quantity']

# 				item = {
# 				'id':product.id,
# 				'product':{'id':product.id,'name':product.name, 'price':product.price, 
# 				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
# 				'digital':product.digital,'get_total':total,
# 				}
# 				items.append(item)

# 				if product.digital == False:
# 					order['shipping'] = True
# 		except:
# 			pass
			
# 	return {'cartItems':cartItems ,'order':order, 'items':items}

# from django.core.exceptions import ObjectDoesNotExist

# def cartData(request):
#     cartItems = 0
#     order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#     items = []

#     if request.user.is_authenticated:
#         try:
#             customer = request.user.customer
#             order, created = Order.objects.get_or_create(customer=customer, complete=False)
#             items = order.orderitem_set.all()
#             cartItems = order.get_cart_items
#         except ObjectDoesNotExist:
#             # Handle the case where the customer does not exist
#             # You can create the customer or take appropriate action based on your application logic
#             # For example:
#             customer = Customer.objects.create(user=request.user)
#             order, created = Order.objects.get_or_create(customer=customer, complete=False)
#             items = order.orderitem_set.all()
#             cartItems = order.get_cart_items
#     else:
#         cookieData = cookieCart(request)
#         cartItems = cookieData['cartItems']
#         order = cookieData['order']
#         items = cookieData['items']

#     return {'cartItems': cartItems, 'order': order, 'items': items}

	
# def guestOrder(request, data):
# 	name = data['form']['name']
# 	email = data['form']['email']

# 	cookieData = cookieCart(request)
# 	items = cookieData['items']

# 	customer, created = Customer.objects.get_or_create(
# 			email=email,
# 			)
# 	customer.name = name
# 	customer.save()

# 	order = Order.objects.create(
# 		customer=customer,
# 		complete=False,
# 		)

# 	for item in items:
# 		product = Product.objects.get(id=item['id'])
# 		orderItem = OrderItem.objects.create(
# 			product=product,
# 			order=order,
# 			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
# 		)
# 	return customer, order

