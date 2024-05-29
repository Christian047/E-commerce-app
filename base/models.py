
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Permission, Group
from core.models import Payment
from django.db.models import Sum



# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    # name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
   
    is_vendor = models.BooleanField(default=True, null=True, blank=True)
    
    def __str__(self):
        return self.username or self.email or str(self.id)
    
      
    def get_vendor_products(self):
        return Product.objects.filter(vendor=self)

class Subscribers(models.Model):
    name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(blank=False)
    
    def __str__(self):
        return self.email
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    balance = models.FloatField(default=0.0)
    description = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def update_balance(self):
        total_payments = Payment.objects.filter(user=self.user).aggregate(Sum('amount'))['amount__sum'] or 0
        self.balance = total_payments
        self.save()
    
class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True, null=True)
    amount = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.description} - {self.date.strftime('%B %Y')}" 
    
    
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, max_length=300)

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name
     
 
post_status = (

    ('pending', "pending"),
    ('delete', "delete"),
    ('approved', "approved")
) 
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    vendor = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_vendor': True})
    status = models.CharField(choices=post_status,default='pending',max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True, max_length=200,null=True)
    likes = models.ManyToManyField(User,related_name='blog_posts')
    favorite = models.ManyToManyField(User,related_name='products')
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.name
  
    def total_likes(self):
        return self.likes.count()
  

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        
    class Meta:
        ordering = ('-created',)





class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    # vendor = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_vendor': True})
    vendor = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_vendor': True}, related_name='vendor_reviews')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True,blank=True)
    rating = models.IntegerField()

    def __str__(self):
        return f"Review by {self.customer.username if self.customer else 'Unknown Customer'} for {self.product.name if self.product else 'Unknown Product'}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='products')
    
    class Meta:
        unique_together = ('user', 'product')

        
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
    def reset_items(self):
        # Assuming you have a related name 'order_items' on the Order model
        self.orderitem_set.all().delete()

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # @property
    # def get_total(self):
        
    #     if self.product and self.product.price:
    #         total = self.product.price * self.quantity
    #         return total
    
    # @property
    # def get_total(self):
    #         if self.product and self.product.price:
    #             total = self.product.price * self.quantity
    #             return total
    #         else:
    #             return 0
            
    @property
    def get_total(self):
        if self.product and self.product.price is not None:
            total = self.product.price * self.quantity
            return total
        else:
            return 0
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address















class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

# create a room model 
class Room(models.Model):
    host = models.ForeignKey(User, on_delete= models.SET_NULL,null= True)
    topic= models.ForeignKey(Topic, on_delete= models.SET_NULL,null= True)
    name = models.CharField(max_length= 200)
    description = models.TextField(null= True, blank= True)
    # many to many field takes the denominator and the related name ensures that
    # it does not clash with an already taken denominator
    participants = models.ManyToManyField(User, related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)
    
    # return by name
    def __str__(self): 
        return self.name
    
    # Arrange by ascending or descending order
    # - reverses the ordering
    class Meta:
        ordering = ['-updated', '-created']
    
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now= True)
    created = models.DateTimeField(auto_now_add= True)
    
    # return by name
    # It also returns the body trimmed to 50 words
    def __str__(self):
        return self.body[0:50]
    
      # Arrange by ascending or descending order
    # - reverses the ordering
    class Meta:
        ordering = ['-updated', '-created']
    
    
    
    