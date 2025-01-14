from django.shortcuts import render, get_object_or_404
from .cart import Cart
from afri_shop.models import Product
from django.http import JsonResponse
from django.contrib import messages

#from .models import Product, Cart

def cart_summary(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.total()

    return render(request, "cart_summary.html",{"cart_products":cart_products, "quantities":quantities,"totals":totals})

def cart_add(request):
  #Getting the cart
  cart = Cart(request)

  #testing the POST
  if request.POST.get('action') == 'post':
      
      #Getting our stuff
      product_id = int(request.POST.get('product_id'))
      product_qty = int(request.POST.get('product_qty', 1))
      #looking product in a database
      product = get_object_or_404(Product, id=product_id)

      #Now saving it to session
      cart.add(product=product, quantity=product_qty)
      
      #Getting the cart quantity
      
      #Returning response
      response = JsonResponse({'Product Name:': product.name})
      messages.success(request,("Great choice! Your item is now in the cart."))
      
      return response
"""
def cart_add(request):
 cart = Cart(request)  

 if request.POST.get('action') == 'post':
     product_id = int(request.POST.get('product_id'))
     quantity = int(request.POST.get('quantity', 1))

     product = get_object_or_404(Product, id=product_id)

     #save session
     #cart.add(product=product)
     cart.add(product_id, quantity)

     #cart_quantity = cart._len_()
     cart_quantity = sum(cart.cart.values())
     response = JsonResponse({'qty:': cart_quantity})
     messages.success(request, 'Product has been added to cart!')
     #response = JsonResponse({'Product Name:': product.name})
     
     return response

"""
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
      
      #Getting our stuff
      product_id = int(request.POST.get('product_id'))
      
      #delete function
      cart.delete(product=product_id)

      response = JsonResponse({'product':product_id})
      messages.success(request,("Item removed. Let us know if you change your mind!"))
      return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
      
      #Getting our stuff
      product_id = int(request.POST.get('product_id'))
      product_qty = int(request.POST.get('product_qty', 1))
 
      cart.update(product= product_id, quantity=product_qty)

      response = JsonResponse({'qty':product_qty})
      messages.success(request,("Cart updated! Happy shopping."))
     
      return response
      
      #return redirect('cart_summary')
    
# Create your views here.
