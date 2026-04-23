import json
import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def index(request):
    featured_products = Product.objects.all().order_by('-created_at')[:4]
    return render(request, 'website/index.html', {'featured_products': featured_products})

def products(request):
    all_products = Product.objects.all().order_by('-created_at')
    return render(request, 'website/products.html', {'products': all_products})

def cart(request):
    return render(request, 'website/cart.html')

def checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        delivery_preference = request.POST.get('delivery_preference')
        address = request.POST.get('address', '')
        instructions = request.POST.get('instructions', '')
        cart_data_raw = request.POST.get('cart_data')
        
        cart_items = json.loads(cart_data_raw)
        
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Save order to DB
        order = Order.objects.create(
            customer_name=full_name,
            phone=phone,
            email=email,
            delivery_preference=delivery_preference,
            address=address,
            instructions=instructions,
            cart_items=cart_items,
            total_amount=total_amount
        )
        
        # Prepare WhatsApp Message
        wa_number = "919767975707"
        message = f"New Order from {full_name}\n"
        message += f"Phone: {phone}\n"
        message += f"Delivery: {'Online Delivery' if delivery_preference == 'delivery' else 'Self Pickup'}\n"
        if delivery_preference == 'delivery':
            message += f"Address: {address}\n"
        message += "\nProducts:\n"
        
        for idx, item in enumerate(cart_items, 1):
            message += f"{idx}. {item['name']} - ₹{item['price']} x {item['quantity']} = ₹{item['price'] * item['quantity']}\n"
            
        message += f"\nTotal: ₹{total_amount}\n"
        if instructions:
            message += f"\nSpecial Instructions: {instructions}"
            
        encoded_message = urllib.parse.quote(message)
        wa_url = f"https://wa.me/{wa_number}?text={encoded_message}"
        
        return render(request, 'website/order_success.html', {'wa_url': wa_url})
        
    return render(request, 'website/checkout.html')

def contact(request):
    return render(request, 'website/contact.html')

from .forms import ProductForm

@staff_member_required
def admin_dashboard(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'website/admin/dashboard.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'website/admin/product_form.html', {'form': form, 'title': 'Add New Product'})

@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'website/admin/product_form.html', {'form': form, 'title': 'Edit Product', 'product': product})

@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('admin_dashboard')

@staff_member_required
def view_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'website/admin/orders.html', {'orders': orders})

@require_POST
def ajax_admin_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data'}, status=400)

    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        if user.is_staff:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/admin-panel/'})
        else:
            return JsonResponse({'success': False, 'error': 'You do not have admin access'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid username or password'})

@require_POST
def ajax_admin_logout(request):
    logout(request)
    return JsonResponse({'success': True})
