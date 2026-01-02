from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    	path('register/', views.register_user, name='register'),
        path('about/', views.about, name='about'),
        path('contact/', views.contact, name='contact'),
    
    	path('update_item/', views.updateItem, name="update_item"),
    	    	path('process_order/', views.processOrder, name="process_order"),
    	        path('order_placed/<int:order_id>/', views.order_placed, name='order_placed'),
        path('order_history/', views.order_history, name='order_history'),
        path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]