from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart



def search(request):
    #Determine if they've filled the form
     if request.method == "POST":
         searched = request.POST['searched']
         #Query the products in database model
         searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
         #Test for null
         if not searched:
            messages.error(request, "Product not found. Please try again.")
            return render(request, "search.html", {})
         else:
            return render(request, "search.html", {'searched':searched})
     else:
      return render(request, "search.html", {})

def update_info(request):
    current_user = request.user
    if request.method == 'POST':
        shipping_user = ShippingAddress.get.objects.get(id=request.user.id)
        form = UserInfoForm(request.POST, instance=current_user.profile)  # Assuming `Profile` is linked to the user
        
        #Getting the user's shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid(   ):
            form.save()
            shipping_form.save()
            messages.success(request, "Your profile information has been successfully updated!")
            return redirect('home')  # Redirect to a profile or success page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserInfoForm(instance=current_user.profile)
        try:
            shipping_user = ShippingAddress.objects.get(id=request.user.id)
            shipping_form = ShippingForm(instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            shipping_form = ShippingForm()  # Create an empty form if no shipping address exists
    
    return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})

  

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            user_form = PasswordChangeForm(current_user, request.POST)
            print(user_form)
            if user_form.is_valid():
                user = user_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, "Your password has been successfully updated!")
                return redirect('update_user')  # Redirect to the desired page after successful password change
            else:
                messages.error(request, "Please correct the errors below.")
                return redirect('update_password')
        else:
            user_form = PasswordChangeForm(current_user)
        
        return render(request, "update_password.html", {'user_form': user_form})
    else:
        messages.error(request, "Please sign in to access this page.")
        return redirect('home')


"""
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Did they fill the form?
        if request.method == 'POST': 
           pass
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {})
    else:
        messages.success(request,("Please sign in to access this page."))
        return redirect('home')
"""

def update_user(request):
    if request.user.is_authenticated:
     current_user = User.objects.get(id=request.user.id )
     user_form = UpdateUserForm (request.POST or None, instance=current_user)
      
     if user_form.is_valid():
        user_form.save()

        login(request, current_user)
        messages.success(request,("User profile updated successfully."))
        return redirect('home')
     return render(request, "update_user.html", {'user_form':user_form})
    else:
       messages.success(request,("Please log in to access this page."))
       return redirect('home')
        
def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html', {"categories":categories})

def category(request, foo):
    #Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    #Grabbing the category from the url
    try:
         #Look up the category
         category = Category.objects.get(name=foo)
         products = Product.objects.filter(category=category)
         return render(request,'category.html', {'products':products, 'category':category})
    except:
        messages.success(request,("Oops! This category doesn’t exist."))
        return redirect('home')
    


def product(request, pk):
   product = Product.objects.get(id=pk)
   return render(request, 'product.html', {'product':product})
 
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password= password)
        if user is not None:
            login(request, user)

            #Lets do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            #Get their saved cart from db
            saved_cart = current_user.old_cart
            #Convert db string to python dict
            
            if saved_cart:
                #convert using JSON {"3:2, "4:1}
                converted_cart = json.loads(saved_cart)
                #adding the loaded cart dictionary to our session
                #Get cart
                cart = Cart(request)
                #Loop throught the cart +  add the items from db
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

     

            messages.success(request,("You're in! Enjoy exploring."))
            return redirect('home')
        else:

            messages.success(request,("Oops! Something went wrong. Double-check your details and give it another go."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You've logged out. Thanks for visiting! Come back anytime for more."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("Registration successful! You can now update your profile information."))
            return redirect('update_info')
        else:
            messages.success(request,("You're so close! Review and give it another go."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

# Create your views here.
