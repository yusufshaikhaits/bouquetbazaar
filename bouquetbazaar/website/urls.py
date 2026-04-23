from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    
    # Custom Admin Panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/add/', views.add_product, name='add_product'),
    path('admin-panel/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('admin-panel/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin-panel/orders/', views.view_orders, name='view_orders'),
    
    # AJAX Auth
    path('admin-login/', views.ajax_admin_login, name='ajax_admin_login'),
    path('admin-logout/', views.ajax_admin_logout, name='ajax_admin_logout'),
]
