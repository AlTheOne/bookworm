from cartApp.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        count_cart = Cart.objects.filter(user=request.user, is_active=True).count()
    else:
        count_cart = Cart.objects.filter(session=request.session.session_key, is_active=True).count()
    return locals()