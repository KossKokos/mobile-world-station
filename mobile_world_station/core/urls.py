from django.urls import path

import core.views as views

app_name = 'core'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.get_home, name='home'),

    path('products/', views.get_products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/summary/', views.cart_summary, name='summary'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),  # You'll need to implement this
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

    # path('accessories/', views.get_accessories, name='accessories'),
    path('services/', views.get_services, name='services'),
    # path('deals/', views.get_deals, name='deals'),
    path('about/', views.get_about, name='about'),
    path('contact/', views.get_contact, name='contact'),
]