# q helps to wrap search parameters
from email import message
from itertools import product
from multiprocessing import context
from django.db.models import Avg

from django.db.models import Q
# Login required Used to restrict users from certain pages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
import json
import datetime
from django.views import View
from django.db.models import Sum
from django.views.generic import DetailView

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse 

from .models import *
from core.models import Payment
from .utils import cookieCart, cartData, guestOrder
import pdb
from django.contrib.auth.mixins import LoginRequiredMixin












# Next function

        

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    total_amount = None  # Initialize total_amount to None
    Product_categories = Category.objects.all()
    approved_products = Product.objects.filter(status='approved')
    approved_products = Product.objects.filter(status='approved').exclude(category__name='Featured post')

    try:
        Featured = Product.objects.filter(category__name='Featured post', status='approved')

    except Product.DoesNotExist:
        Featured = None

    if request.user.is_authenticated:
        user_wallet, created = Wallet.objects.get_or_create(user=request.user)
    else:
        user_wallet = None

    if request.user.is_authenticated:
        try:
            total_amount = Payment.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
        except Exception as e:
            print(f"An error occurred: {e}")
          
        pending_post = Product.objects.filter(status='pending')
        
        
       
        try:
            userpendingproducts = Post.objects.filter(author=request.user, status='pending')
        except:userpendingproducts=None
        
        try:
            userproducts = Post.objects.filter(author=request.user, status='approved')
        except: userproducts = None
        

        income_list = Wallet.objects.filter(user=request.user)
        expenses_list = Expenses.objects.filter(user=request.user)
        sum_total_income = income_list.aggregate(sum_total_income=Sum('balance'))['sum_total_income'] or 0

        # Calculate sum_total_expense only if the user is authenticated
        sum_total_expense = expenses_list.aggregate(sum_total_expense=Sum('amount'))['sum_total_expense'] or 0
    else:
        income_list = []
        expenses_list = []
        sum_total_income = 0
        sum_total_expense = 0

    products = Product.objects.all()
    context = {'products': products,
               'cartItems': cartItems,
               'income_list': income_list,
               'expenses_list': expenses_list,
               'sum_total_income': sum_total_income,
               'sum_total_expense': sum_total_expense,
               'total_amount': total_amount,  
               'Product_categories': Product_categories, 
               'approved_products': approved_products, 
               'Featured': Featured, 
               'user_wallet': user_wallet, 
               }
    return render(request, 'base/store.html', context)




@login_required(login_url='login')
def Category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect('store')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'category/category_form.html', context)




class Category_list(DetailView):
    def get(self, request, category_slug):
        Product_categories = Category.objects.all()
        catlist = Category.objects.get(slug=category_slug)
        category_by_post = Product.objects.filter(category=catlist, status='approved')
        contexta = {
            'list': catlist,              
            'Product_categories': Product_categories,               
            'category_by_post': category_by_post, 
        }

        return render(request, 'category/cat_list.html', context=contexta)

    def post(self, request):
        return render(request, 'category/cat_list.html')


@login_required(login_url='login')
def LikeView(request, pk):
    product = get_object_or_404(Product, id=request.POST.get('product_id'))

    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        liked = False
    else:
        product.likes.add(request.user)
        liked = True
    print(request.POST)


    return HttpResponseRedirect(reverse('eachproduct', args=[str(pk)]))




@csrf_exempt
def update_user_order(request):
    if request.method == 'POST':
        # Extract data from the request
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']

        product = Product.objects.get(id=productId)
        purchase_amount = product.price

        # Assuming you have an Order model, update the order here
        # ...

        # Subtract the purchase amount from the user's wallet
        user_profile = request.user.userprofile
        subtract_from_wallet(user_profile, purchase_amount)

        # Return a JsonResponse with any data you want to send back to the frontend
        return JsonResponse({'status': 'success', 'purchaseAmount': purchase_amount})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    
    
    
    

class IncomeCreateView(View):
       

    def get(self, request):
        return render(request,'incomexp/income_create.html')

    def post(self, request):
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        incometype_id = request.POST.get('incometype')

        Wallet.objects.create(
            user=request.user,
            balance=amount,
        
        )
        return redirect('store')

@login_required(login_url= 'login')
def add_review(request, product_id):
    page = 'add_review'
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.customer = request.user.customer  # Assuming you have a one-to-one relationship between User and Customer
            review.save()
            return redirect('eachproduct', pk=product_id)  # Redirect to the product detail page
    else:
        form = ReviewForm()

    return render(request, 'base/add_review.html', {'form': form, 'product': product,'page' : page})



@login_required(login_url= 'login')
def add_vendor_review(request,vendor_id):
    vendor = get_object_or_404(Customer, pk=vendor_id)
    

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.vendor = vendor
            review.customer = request.user.customer  
            review.save()
            return redirect('vendor_products', vendor_id=vendor_id)

  # Redirect to the product detail page
    else:
        form = ReviewForm()

    return render(request, 'base/add_vendor_review.html', {'form': form, 'vendor': vendor})



@login_required(login_url='login')
def update_review(request,pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('eachproduct', pk=review.product.pk)


    else:
        form = ReviewForm(instance=review)

    context = {'form': form, 'review': review}
    return render(request, 'base/add_review.html', context)

@login_required(login_url= 'login')
def delete_review(request,pk):

    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'review deleted')
        if request.user.customer.is_vendor:
            return redirect('Vendor_dashboard')
        else:
            return redirect('store')
    return render(request, 'base/delete.html', {'obj' : review})



def Vendor_dashboard(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'base/Vendor_dashboard.html', context)





@login_required(login_url= 'login')
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'base/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'base/checkout.html', context)


def Confirm_order(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'base/Confirm_order.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)




# 
def Subtract_amount(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Assuming each order has an associated total amount
    purchase_amount = order.get_cart_total
    
    # Retrieve the user's wallet or create one if it doesn't exist
    user_wallet, created = Wallet.objects.get_or_create(user=request.user)
    
    # Check if the wallet has sufficient funds
    if user_wallet.balance >= purchase_amount:
        # Subtract the purchase amount from the wallet balance
        user_wallet.balance -= purchase_amount
        user_wallet.save()

        # Perform other actions related to confirming the purchase

        messages.success(request, 'Purchase confirmed successfully!')
        
        # Create an expense record
        Expenses.objects.create(user=request.user, amount=float(purchase_amount))
        
        # Reset order items to zero (assuming you have an appropriate method for this)
        order.reset_items()
        return redirect('store')  # Redirect to a success page
    else:
        # Insufficient funds, return an error message
        messages.error(request, 'Insufficient funds in your wallet!')
        # Redirect to an error page
        return redirect('cart')  # Mak
    
     
    
    


# function to create particular rooms
def Eachproduct(request, pk):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # Retrieve the product or return a 404 response if not found
    product = get_object_or_404(Product, id=pk)

    # Retrieve all reviews for the product
    product_reviews = Review.objects.filter(product=product)

    # Calculate the average rating for the product
    average_rating = product_reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    # Check if the current user has liked the product
    liked = False
    if request.user.is_authenticated:
        liked = product.likes.filter(id=request.user.id).exists()

    # Add the 'stars' attribute to each review
    for review in product_reviews:
        review.stars = range(review.rating)

    # Pass variables to the context dictionary
    context = {
        'product': product,
        'product_reviews': product_reviews,
        'number_of_reviews': product_reviews.count(),
        'liked': liked,
        'total_likes': product.total_likes(),
        'average_rating': average_rating,
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }

    # Render the template with the provided context
    return render(request, 'base/product.html', context)



def vendor_products(request, vendor_id):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # Assuming you have a URL pattern that captures the vendor_id
    # Retrieve the vendor based on the vendor_id
    vendor = Customer.objects.get(pk=vendor_id)
    vendor_reviews = Review.objects.filter(vendor=vendor)

    # Retrieve all products associated with the vendor
    products = vendor.get_vendor_products()

    # Render the template with the vendor's products
    return render(request, 'base/vendor_products.html', {'vendor': vendor,'vendor_reviews': vendor_reviews, 'products': products,      'cartItems': cartItems,
        'order': order,
        'items': items,})




# Use login required to restrict unauthenticated users
from django.shortcuts import render, redirect
from .forms import ProductForm  # Import your ProductForm

@login_required(login_url='login')
def create_product(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Create the product form with the submitted data
        form = ProductForm(request.POST, request.FILES)

        # Check if the form is valid
        if form.is_valid():
            # Create a new product object but don't save it to the database yet
            product = form.save(commit=False)

            # Check if the current user's customer is also a vendor
            if request.user.customer.is_vendor:
        # If the customer is a vendor, assign the vendor to the product
               product.vendor = request.user.customer

            else:
                # Handle the case where the customer is not a vendor (you may choose to do something else)
                pass

            # Save the product to the database
            product.save()

            # Redirect to a different page
            return redirect('store')
    else:
        # If the request method is not POST, create an empty form
        form = ProductForm()

    context = {'form': form}
    return render(request, 'base/product_form.html', context)


@login_required(login_url='login')
def update_product(request,pk):
    # Get the product instance by ID
    product = get_object_or_404(Product, id=pk)

    # Check if the request method is POST
    if request.method == 'POST':
        # Create the product form with the submitted data and instance
        form = ProductForm(request.POST, request.FILES, instance=product)

        # Check if the form is valid
        if form.is_valid():
            # Save the updated product to the database
            form.save()

            # Redirect to a different page (you can choose where to redirect)
            return redirect('store')

    else:
        # If the request method is not POST, create a form with the current product instance
        form = ProductForm(instance=product)

    context = {'form': form}
    return render(request, 'base/product_form.html', context)

# create an updateRoom function
# function to delete room taking unique parameters
@login_required(login_url= 'login')
def delete_product(request,pk):
    
    # query the database to get the unique room and pass to variable
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        # use delete method and return to homepage
        product.delete()
        messages.success(request, 'Product deleted')
        return redirect('store')
    # return the template and pass in direct context
    return render(request, 'base/delete.html', {'obj' : product})



from email.message import EmailMessage
import ssl,smtplib


def subscribe(request):
    if request.method == 'POST':
        # Fetch the form data
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Your email sending logic
        send_email(name, email)
        Subscribers.objects.create(name=name, email=email)

        # You might also want to redirect the user or display a success message
        return render(request, 'base/store.html', {'success': True})

    return render(request, 'base/store.html', {'success': False})



    
    
def send_email(name, email):
    # Your email sending logic
    email_sender = 'Padigachris@gmail.com'
    email_password = 'eivt sumy iaic okwh'
    email_receiver = email
    subject = 'Thanks for subscribing'
    body = f'Thanks for subscibing, {name}!'

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_bytes())
        print('Message sent')





def suscribers_list(request):
   suscribers = Subscribers.objects.all()
   context ={'suscribers': suscribers}
   return render(request,'base/Suscribers.html', context)
    

























# function to direct to the home page
def home1(request):
    # assign a variable to a subject of the database query
    # check if the database request is not empty
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # queries the database based on the variable and assigns to q that will be called in the template
    # (Search Filter) icontains is a kind of search functionality that auto completes search tasks
    # Q enables for multiple exclusive searches
    rooms = Room.objects.filter(
                                Q(topic__name__icontains = q) |
                                Q(name__icontains = q)   |
                                Q(description__icontains = q))

    # gets all the Topics objects and puts them in a variable
    topics = Topic.objects.all()[0:5]
    topic_count = Topic.objects.all()
    
    # count number of rooms by using count method or len method
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    # Puts them in a context to display to the home page
    contexta = {'rooms': rooms, 'topics': topics, 'room_count' :  room_count, 'room_messages': room_messages,'topic_count': topic_count}
    # returns the homepage template with a request and a context parameter
    return render(request, 'base/store.html',contexta)

# function to create particular rooms
def room(request,pk):
    # queries the database, based on a particular key assigns it to a variable
    room= Room.objects.get(id= pk)
    '''Get messages a model child of the room(in lower case), returns the set of the messages
    associated with the room
    
    Gets all the message_set associated with the romm'''
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    # Check for post requests from a form
    if request.method== 'POST':
        # Use a create object to create an object that will be stored in the model 
        # and outputted in the template
        # The create method takes in the parameters that it needs to create
        message = Message.objects.create(
            user = request.user,
            room= room,
            body = request.POST.get('body')
        )
        
        room.participants.add(request.user)
        # return to the particular room
        # redirect can take two parameters ,wh
        return redirect('room',pk =room.id)
   
    # passes that variable to a context
    # variables that are to be called in the template are added in context
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    # returns the unique template with a context
    return render(request, 'base/room.html', context)


# Function to display user profile
def userProfile(request,pk):
    # Get a particular user from Django inbuilt user model
    user = User.objects.get(id = pk)
    # get all the room model objects associated with the user
    rooms = user.room_set.all()
    # get all the messages attributed to the user
    room_messages = user.message_set.all()
    # Get all topics
    topics = Topic.objects.all()
    
    
    context ={'user': user,'rooms':rooms, 'room_messages': room_messages,'topics': topics}
    return render(request,'base/profile.html', context)





# Use login required to restrict unauthenticated users
# login url redirects users to a certain page
@login_required(login_url= 'login')

# Function to create a room
def create_room(request):
    
    # gets the form already created and passes it to a variable
    form = Roomform()
    
    # Get all the topics in the database
    topics = Topic.objects.all()
    
    # check if the post method is called
    if request.method == 'POST':
        
        # query the input and assign the inputted topic to topic_name 
        topic_name = request.POST.get('topic')
        # Get or create method queries the database and assigns variables to either the instances
        # In this case if the topicname is queried if not exist it is created
        topic,created = Topic.objects.get_or_create(name =topic_name)
        # form takes on the particulars submited in the template form
        form = Roomform(request.POST)
        
        # Create method creates objects directly to the database
        Room.objects.create(
            # The host is assigned to the current user
            host =request.user,
            # get the topic from the request.post bracket
            topic = topic,
            name= request.POST.get('name'),       
            description = request.POST.get('description'),       
        )
        
        return redirect('home')
        # check if the form is valid 
        # if form.is_valid():
        #     # Give a false commit and extract the information of the room
        #     room = form.save(commit=False)
        #     # assign the room host title to the current user
        #     room.host = request.user
        #     # save room
        #     room.save()
            # redirect to a different page
            # return redirect('home')
        
        
        
    context = {'form': form, 'topics': topics}  # Add the form to the context
    return render(request, 'base/room_form.html', context)


# create an updateRoom function
@login_required(login_url= 'login')
def updateRoom(request, pk):
    # query the Room model by the primary key and assign to a variable
    room = Room.objects.get(id=pk)
    # Initialize the form to be prefilled with its unique objects using its room variable
    form = Roomform(instance=room)
    
    # Get all the topics in the database
    topics = Topic.objects.all()
    
    """ check if the logged in user is the room author
    and authorized to edit rooms"""
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    # check the form of request
    if request.method == 'POST':
        # query the input and assign the inputted topic to topic_name 
        topic_name = request.POST.get('topic')
        # Get or create method queries the database and assigns variables to either the instances
        # In this case if the topicname is queried if not exist it is created
        topic,created = Topic.objects.get_or_create(name =topic_name)
    #   get the input forms and overide the current variables
        room.name= request.POST.get('topic')
        # assign the topic from an already gotten get or create variable
        room.topic= topic
        room.description= request.POST.get('description')
        room.name= request.POST.get('topic')
        
        # Save the overidden form using the save method
        room.save()
        
    
        return redirect('home')
           
    # create a context for template rendering
    context = {'form': form, 'topics': topics, 'room':room}
    # Return the template
    return render(request, 'base/room_form.html', context)



# function to delete room taking unique parameters
@login_required(login_url= 'login')
def deleteRoom(request,pk):
    
    # query the database to get the unique room and pass to variable
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        # use delete method and return to homepage
        room.delete()
        return redirect('home')
    # return the template and pass in direct context
    return render(request, 'base/delete.html', {'obj' : room})

@login_required(login_url= 'login')
def deleteMessage(request,pk):
    
    # query the database and get the unique message 
    message= Message.objects.get(id = pk)
    
    # Check if the logged in user is the same as the message poster
    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        # use delete method and return to homepage
        message.delete()
        return redirect('home')
    # return the template and pass in direct context
    return render(request, 'base/delete.html', {'obj' : message})


@login_required(login_url= 'login')
def updateUser(request):
    user = request.user
    # Instance parameter is passed to ensure that it brings up the unique user
    form = Userform(instance=user)
    # if a post request is being made,form variable is assigned to collect the information
    if request.method =='POST':
        
        form = Userform(request.POST, instance=user)
        if form.is_valid:

            form.save()
            # it saves and redirects to the current user
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html',{'form': form})


def topicsPage(request):
    # q is put in because it is a search
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # filters the database and gets the variable passed in the get method
    topics = Topic.objects.filter(name__icontains =q)
    
    
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    # Call in the messages from the models
    # because its not a global variable
    room_messages = Message.objects.all()
    
    return render(request, 'base/activity.html', {'room_messages': room_messages })






class Pendingpage(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        if request.user.is_staff:
            pending_products = Product.objects.filter(status='pending')
        else:
            pending_products = Product.objects.filter(author=request.user, status='pending')
        return render(request, 'base/pendingpage.html', {'pending_products': pending_products})
            
    def post(self, request, pk=None):
        if request.user.is_staff:
           pending_product = get_object_or_404(Product, pk=pk)
  
        if request.method == 'POST':
            pending_product.status = 'approved'
            pending_product.save()
    
            return redirect('penpage')
        else:
            messages.error(request, 'You do not have permission to perform this action.')
        return redirect('penpage') 




class UnapproveProduct(LoginRequiredMixin, View): 
    login_url = 'login'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'POST':
            product.status = 'pending'
            product.save()
            messages.success(request, 'Product unapproved successfully.')
        else:
            messages.warning(request, 'Invalid request to unapprove the product.')

        return redirect('store')
