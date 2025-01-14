from afri_shop.models import Product, Profile

class Cart:
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request
        self.cart = self.session.get('cart', {})

    def db_add(self, product, quantity):
        product_id = str(product) 
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] =  product_qty
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

        #Deal with logged in users
        if self.request.user.is_authenticated:
           #Getting the current user profile
           current_user = Profile.objects.filter(user__id=self.request.user.id)
           carty  =str(self.cart)
           carty = carty.replace("\'", "\"")
           #save carty to profile model
           current_user.update(old_cart=str(carty))

       

    def add(self, product, quantity=1):
        product_id = str(product.id)  # Always store the ID as a string
        product_qty = int(quantity)
            
        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            #self.cart[product_id] = quantity
             self.cart[product_id] = product_qty
            
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

        #Deal with logged in users
        if self.request.user.is_authenticated:
           #Getting the current user profile
           current_user = Profile.objects.filter(user__id=self.request.user.id)
           carty  =str(self.cart)
           carty = carty.replace("\'", "\"")
           #save carty to profile model
           current_user.update(old_cart=str(carty))



    def total(self):
     # Get product IDs and filter the products
         product_ids = self.cart.keys()
         products = Product.objects.filter(id__in=product_ids)
        
         total = 0  # Initialize total
        
         # Loop through the products to calculate the total
         for product in products:
            # Use the product ID to get the corresponding value from the cart
           #cart_item = self.cart.get(str(product.id), {})  # Get the cart item (likely a dict)
             
           #quantity = cart_item.get('quantity', 0)  # Extract the 'quantity' field
           quantity = self.cart.get(str(product.id), 0)
           total += product.price * quantity  # Multiply price by quantity and add to total
        
         return total




    def get_prods(self):
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)


    def __len__(self):
     return sum(item['quantity'] for item in self.cart.values()) 
    #Get ids from cart
    
    def get_prods(self):
     product_ids = self.cart.keys()
    #Use ids to lookup products ind db model
     products = Product.objects.filter(id__in=product_ids)
     return products
    
    def get_quants(self):
       quantities = self.cart
       return quantities
    


    def update(self, product, quantity):
       product_id = str(product)
       product_qty = int(quantity)

       ourcart = self.cart
       ourcart[product_id] = product_qty

       self.session.modified = True

        
         #Deal with logged in users
       if self.request.user.is_authenticated:
        #Getting the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        carty  =str(self.cart)
        carty = carty.replace("\'", "\"")
        #save carty to profile model
        current_user.update(old_cart=str(carty))

        thing = self.cart
       return thing

    
    
    def delete(self,product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        #Deal with logged in users
        if self.request.user.is_authenticated:
           #Getting the current user profile
           current_user = Profile.objects.filter(user__id=self.request.user.id)
           carty  =str(self.cart)
           carty = carty.replace("\'", "\"")
           #save carty to profile model
           current_user.update(old_cart=str(carty))
           

    
    


        