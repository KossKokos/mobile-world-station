from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import json

from .forms import CheckoutForm

from .models import Item, Cart, Order, OrderItem
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')  # Redirect to your products page
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


def get_home(request):
    return render(request=request, template_name='core/home.html')

def get_products(request):

    items = Item.objects.all().values(
        'id',
        'item_name',
        'item_price',
        'item_description',
        'item_image',
        'item_brand',
        'item_type',
        'item_quantity'
    )

    items_list = list(items)

    context = {
        'products': items_list,
        'products_count': len(items_list)
    }

    return render(request=request, template_name='core/products.html', context=context)


def product_detail(request, product_id):
    product = get_object_or_404(Item, pk=product_id)
    
    # Create a list of field names and values for the table
    fields = [
        ('Name', product.item_name),
        ('Price', f"£{product.item_price}"),
        ('Description', product.item_description),
        ('Brand', product.get_item_brand_display()),
        ('Type', product.get_item_type_display()),
        ('Quantity', product.item_quantity),
        # ('Created At', product.created_at.strftime("%Y-%m-%d %H:%M:%S")),
    ]
    
    context = {
        'product': product,
        'fields': fields,
        'in_cart': False    
    }

    if request.user.is_authenticated:
        context['in_cart'] = Cart.objects.filter(
            user=request.user, 
            product=product
        ).exists()

    return render(request, 'core/product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Item, pk=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return JsonResponse({'success': True, 'message': 'Item added to cart', 'cartQuantity': cart_item.quantity})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('product')
    total_price = sum(item.product.item_price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'items_count': cart_items.count()
    }
    return render(request, 'core/cart.html', context)

@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.delete()
        
        # Get updated cart info
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.item_price * item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'items_count': cart_items.count(),
            'total_price': total_price
        })
    return JsonResponse({'success': False}, status=400)

@login_required
# @require_POST
# @csrf_exempt  # Temporarily for testing - remove in production!
def update_cart(request, product_id):
    try:
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'}, status=400)
            
        cart_item = Cart.objects.get(user=request.user, product_id=product_id)
        # check if entered quantity is not bigger than actual of the product
        if quantity > cart_item.product.item_quantity:
            return JsonResponse({'success': False, 'error': 'Quantity is bigger than actual'}, status=406)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'quantity': quantity,
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
    except (ValueError, json.JSONDecodeError) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
  

@login_required
def cart_summary(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product_price for item in cart_items)
    
    return JsonResponse({
        'success': True,
        'items_count': cart_items.count(),
        'total_price': total_price
    })

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return redirect('core:view_cart')
    
    total_price = sum(item.product_price for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=form.cleaned_data['shipping_address'],
                payment_method=form.cleaned_data['payment_method']
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.item_price
                )
            
            # Clear cart
            cart_items.delete()
            
            # Redirect to order confirmation
            return redirect('core:order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'core/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_confirmation.html', {'order': order})


def get_accessories(request):
    return render(request=request, template_name='core/accessories.html')

def get_services(request):
    return render(request=request, template_name='core/services.html')

def get_deals(request):
    return render(request=request, template_name='core/deals.html')

def get_about(request):
    return render(request=request, template_name='core/about.html')

def get_contact(request):
    return render(request=request, template_name='core/contact.html')
