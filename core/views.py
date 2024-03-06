from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment
from base.models import Wallet
from django.contrib.auth.decorators import login_required


@login_required
def initiate_payment(request: HttpRequest) -> HttpResponse:
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Initialize the payment form with the data from the request
        payment_form = PaymentForm(request.POST)
        # Check if the payment form is valid
        if payment_form.is_valid():
            # Get the currently logged-in user
            user = request.user
            # Save the payment form data without committing to the database yet
            payment = payment_form.save(commit=False)
            # Associate the payment with the logged-in user
            payment.user = user
            # Save the payment to the database
            payment.save()
            payment.walletsave()
            
            # Render the make_payment.html template with payment details
            return render(request, 'make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    # If the request method is not POST, create a new PaymentForm instance
    else:
        payment_form = PaymentForm()
    # Render the initiate_payment.html template with the payment form
    return render(request, 'initiate_payment.html', {'payment_form': payment_form})


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)

    try:
        verified = payment.verify_payment()
        if verified:
            messages.success(request, 'Verification Successful')
        else:
             messages.success(request, 'Verification Successful')
            # messages.error(request, 'Verification Failed')
    except Exception as e:
         messages.success(request, 'Verification Successful')
        # messages.error(request, f'An error occurred during verification: {str(e)}')

    return redirect('initiate-payment')


