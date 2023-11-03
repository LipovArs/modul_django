from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Product, UserProfile, OrderItem, Return
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PurchaseForm
from django.utils import timezone

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            custom_user = UserProfile(user=user, balance=10000)
            custom_user.save()
            return redirect('home_page')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    balance = user.userprofile.balance
    orders = OrderItem.objects.filter(user=user)
    return render(request, 'shop/profile.html', {'user': user, 'balance': balance, 'orders': orders})


def create_order(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        if purchase_form.is_valid():
            quantity = purchase_form.cleaned_data['quantity']

            if product.quantity >= quantity and request.user.userprofile.balance >= product.price * quantity:

                order_item = OrderItem(user=request.user, product=product, quantity=quantity)
                order_item.save()

                product.quantity -= quantity
                product.save()

                request.user.userprofile.balance -= product.price * quantity
                request.user.userprofile.save()

                return redirect('profile')
            else:
                return render(request, 'shop/purchase_error.html')
    else:
        purchase_form = PurchaseForm()

    return render(request, 'shop/purchase.html', {'purchase_form': purchase_form, 'product': product})


def return_item(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    purchase_time = order_item.created_at
    current_time = timezone.now()
    time_difference = current_time - purchase_time

    if time_difference.total_seconds() <= 180:
        return_obj = Return(purchase=order_item)
        return_obj.save()
        return redirect('profile')
    else:
        return render(request, 'shop/return_error.html')


def confirm_return(request, return_id):
    return_obj = Return.objects.get(id=return_id)

    if return_obj.status == 'на розгляді':
        order_item = return_obj.purchase
        user = order_item.user

        user_profile = UserProfile.objects.get(user=user)
        user_profile.balance += order_item.product.price * order_item.quantity
        user_profile.save()

        product = order_item.product
        product.quantity += order_item.quantity
        product.save()

        return_obj.status = 'підтверджено'
        return_obj.admin_approved = True
        return_obj.save()

    return redirect('return_list')