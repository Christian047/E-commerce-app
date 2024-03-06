from django.shortcuts import render
# q helps to wrap search parameters
# Login required Used to restrict users from certain pages
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# User is imported from the models to match the user input
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from base.forms import *

from django.views import View


from django.shortcuts import render, redirect

from django.contrib import messages
from .models import *




# Create your views here.

class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base/login_register.html')

    def post(self, request, *args, **kwargs):
        # Retrieve data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Include password field in your form
        address = request.POST.get('address')  # Include password field in your form

        # Convert the is_vendor value to a boolean
        is_vendor = bool(request.POST.get('is_vendor'))

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Authenticate and log in the user
        # No need to authenticate again since the user is already created
        # Just use the user object created above
        login(request, user)

        messages.success(request, 'Registration successful. Welcome!')

        # Check if the user is a vendor
        if is_vendor:
            # Create or update the user profile for vendors
            profile, profile_created = Customer.objects.get_or_create(user=user)
            profile.username = username
            profile.is_vendor = is_vendor
            profile.save()

            messages.success(request, 'Vendor registration successful. Welcome!')
            return redirect('store')  # Replace with your vendor dashboard URL
        else:
            # Replace 'home' with the actual URL name of your home page
            return redirect('store')

        messages.error(request, 'Registration failed. Please check the form.')
        return render(request, 'base/login_register.html')

def loginPage(request):
    # assign a login value to the page to be called in later template
    page = 'login'

    # redirect a logged in user who tries to access this page from anywhere
    if request.user.is_authenticated:
        return redirect('store')

    # check if a user posted
    if request.method == 'POST':
        # Get the input information and put it in a variable
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Use a try method for probable odd returns
        try:
            # assign a user variable to the user object on the basis that the
            # username supplied matches with the one supplied by the user
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Error message takes a request, then a message body
            messages.error(request, 'User does not exist')
            return redirect('login')  # Redirect back to login page if user does not exist
        messages.success(request, "login successful." )

        # authenticate user using the request, username, and password
        user = authenticate(request, username=username, password=password)

        # Check if there is a variable assigned
        # use the login method to login the user
        if user:
            login(request, user)

            # Check if the user is a vendor
            try:
                is_vendor = user.customer.is_vendor
            except Customer.DoesNotExist:
                is_vendor = False

          
            return redirect('store')  # Redirect to vendor dashboard if the user is a vendor
            # Redirect to the store if the user is not a vendor
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    # return the primary page
    return render(request, 'base/login_register.html', context)


# logout function
# assign return page after assigning function
def logoutUser(request):
    # logs out the user and takes request as a parameter
    logout(request)
    return redirect('store')
    
    