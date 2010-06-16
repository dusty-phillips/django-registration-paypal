
def pay_with_paypal(request, username):
    from django.http import HttpResponse
    return HttpResponse("paying with paypal today, are we?")
