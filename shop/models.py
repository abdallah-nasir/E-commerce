from django import template
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime
import uuid
from google_currency import convert
import json

# Create your models here.

    

        
class Customer(models.Model):
    user = models.OneToOneField(User,default=1,on_delete=models.CASCADE)
    first_name=models.CharField(blank=True,null=True,max_length=50)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    street=models.CharField(max_length=100,blank=True,null=True)
    zip=models.CharField(max_length=10,blank=True,null=True)
    country=models.CharField(max_length=20,blank=True,null=True)
    city=models.CharField(max_length=20,blank=True,null=True)
    tel=models.CharField(max_length=50,blank=True,null=True)
  
    def __str__(self):
        return self.user.username
      

@receiver(post_save, sender=User)
def create_user_Customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
class Size(models.Model):
    size=models.CharField(max_length=50)
    def __str__(self):
        return self.size 

class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):     
        return self.name

    @property
    def category_name(self):
        return Product.objects.filter(category__name=self.name)   
  
class Brands(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
    @property
    def brands_name(self):
        return Product.objects.filter(brand__name=self.name)

class Colors(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
    @property     
    def colors_name(self):
        return Product.objects.filter(color__name=self.name)
  
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    size=models.ManyToManyField(Size,blank=True)
    image=models.ImageField()
    details=models.TextField()       
    views=models.PositiveIntegerField(default=0)
    category=models.ForeignKey(Category,null=True,blank=True,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brands,null=True,blank=True ,on_delete=models.CASCADE)
    color=models.ForeignKey(Colors,null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.name                           
    class Meta:
        ordering=["-views"]
    @property
    def same_name(self):
        return Product.objects.filter(category__name=self.category.name)
    @property
    def product_order(self):
        return Product.objects.filter(category__name=self.category.name).order_by("-views")

    def get_same_item(self):
        item=Product.objects.filter(category=self.category)      
        return item

class OrderProduct(models.Model):
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Product,null=True,blank=True,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    device= models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.item.name    
     
    def get_item_price(self):
        price= self.quantity * self.item.price
        return price 


class Coupon(models.Model):
    name=models.CharField(unique=True,max_length=50)
    price=models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    expire_date = models.DateField()
    # orders=models.ManyToManyField(Order,blank=True)
    # user= models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.name
    # def get_total_order_discount(self):
    
class Order(models.Model):
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderProduct)
    order_date = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    price=models.PositiveIntegerField(default=0)
    device= models.CharField(max_length=200,blank=True,null=True)
    coupon=models.ForeignKey(Coupon,blank=True,null=True,on_delete=models.SET_NULL)
    # manager=models.Manager()
    # delete=OrderManager()
    def __str__(self):
        return str(self.id)
           

    def get_order_items(self):
        price=0
        for i in self.items.all():
            price+=i.get_item_price()
        return price
    def get_total_price(self):     
        price=0
        if self.coupon:  
            price+=self.get_order_items()-self.coupon.price

        else:
            for i in self.items.all():
                price+=i.get_item_price()

        return price
    def discount(self):
        if self.coupon:
            count=self.items.all().count()
            coupon=self.coupon.price / count      
        else:
            coupon=0   
        return coupon 
    def converter(self):
        converter=json.loads(convert('egp', 'usd', self.get_total_price())) #to transefer to JSON data
        return converter["amount"]
    # def get_total_discount(self):
    #     coupon=Coupon.objects.filter(user=self.user,orders=self)
    #     if coupon.exists():
    #         disount=self.get_total_price() -100
    #         return disount

 
class WishList(models.Model):
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)
    item = models.ManyToManyField(Product)
    click=models.BooleanField(default=False)
    device= models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
 
        return str(self.id)
       

    def get_absolute_wish(self):
        return redirect(reverse("shop:wishlist",kwargs={"id":self.id}))
CHOICES=(
    ("PREPARED","BEING PREPARED"),
    ("RECEIVED","RECEIVED"),
    ("CANCELLED","CANCELLED"),
    ("HOLD","ON HOLD")
)
class final_order(models.Model):
    name=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,blank=True,on_delete=models.CASCADE)
    money=models.CharField(max_length=100)
    customer_email=models.EmailField(max_length=100,blank=True,null=True)
    payment_intent=models.CharField(blank=True,null=True,max_length=100)
    city=models.CharField(max_length=100,blank=True,null=True)
    country= models.CharField(max_length=100,blank=True,null=True)
    line1= models.CharField(max_length=100,blank=True,null=True)
    line2= models.CharField(max_length=100,blank=True,null=True)
    postal_code= models.CharField(max_length=100,blank=True,null=True)
    ordered=models.BooleanField(default=False)   
    status=models.CharField(choices=CHOICES,max_length=50,default="PREPARED")
    def __str__(self):
        return (f"{self.name} {self.id}")
