from django.shortcuts import render_to_response

def pay_with_paypal(request, username):
    return render_to_response("registration/pay_with_paypal.html")
