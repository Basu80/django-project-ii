import json
from .models import *

def cartData(request):
	if request.user.is_authenticated:
		try:
			customer = request.user.customer
		except:
			customer, created = Customer.objects.get_or_create(user=request.user)
			if created:
				customer.email = request.user.email
				customer.save()
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	return {'cartItems':cartItems ,'order':order, 'items':items}
