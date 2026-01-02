from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cartData
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('store')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']

	search_query = request.GET.get('q')
	if search_query:
		products = Product.objects.filter(name__icontains=search_query)
	else:
		products = Product.objects.all()
		
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	if not request.user.is_authenticated:
		return JsonResponse({'error': 'User is not authenticated'}, status=403)
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

@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	if request.method == 'POST':
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		order.transaction_id = transaction_id
		
		customer.name = request.POST.get('name', customer.name)
		customer.email = request.POST.get('email', customer.email)
		customer.save()
		order.complete = True
		order.save()

		# Always attempt to create a ShippingAddress if address is provided
		if request.POST.get('address'):
			ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=request.POST['address'],
			city=request.POST['city'],
			state=request.POST['state'],
			zipcode=request.POST['zipcode'],
			phone_number=request.POST.get('phone_number', '')
			)
		return redirect('order_placed', order_id=order.id)
	else:
		return redirect('checkout')

def order_placed(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'order': order}
    return render(request, 'store/order_placed.html', context)


def about(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'store/about.html', context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}
    return render(request, 'store/contact.html', context)

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer, complete=True)
    context = {'orders': orders}
    return render(request, 'store/order_history.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user.customer, complete=True)
    context = {'order': order}
    return render(request, 'store/order_detail.html', context)