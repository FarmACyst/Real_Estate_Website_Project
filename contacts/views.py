from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
# Create your views here.

def contact(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made an enquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already made an enquiry for this listing")
                return redirect('listing',listing_id=listing_id)
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email,
        phone=phone, message=message, user_id=user_id)
        contact.save()
        # Send Email
        send_mail(
            "Property Listing Enquiry",
            "There has been an enquiry for "+ listing +". Sign into the admin panel for more info",
            "arbaz05@gmail.com",
            [realtor_email],
            fail_silently = False
        )
        send_mail(
            "Enquiry Sent",
            "Hi "+name+", your enquiry has been sent. A realtor will get back to you.",
            "arbaz05@gmail.com",
            [email],
            fail_silently = False
        )
        messages.success(request, "Your request has been submitted, a realtor will get back to you soon")
        return redirect('listing',listing_id=listing_id)
