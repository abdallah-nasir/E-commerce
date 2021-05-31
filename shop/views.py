from django.http.response import HttpResponseRedirect, JsonResponse
import requests
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.db.models import Count,Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
# from allauth.account.models import EmailAddress
from .models import *
from .filters import *
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as my_login
from .forms import *
from allauth.account.views import SignupView,LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.views import View
from django.http import JsonResponse,HttpResponse
import stripe

# Create your views here.
  
# def get_category_count():
#     qs = Product.objects.values("category__name").annotate(Count("category"))
#     return qs
 
# def get_query(self,id):
#     my_list=WishList.objects.get(user=request.user)
#     context={"list":my_list}
#     return render(request,"base.html",context)
   
   

# def search(request):
#     empty=[]
#     product = Product.objects.all()
#     # latest = Post.objects.order_by("-timestamp")[0:3]
#     # category_count = get_category_count()
#     qs = request.GET.get("q")
#     if qs:
#         my_product = product.filter(Q(color__name=qs)).distinct()
#     if qs =="" or qs ==" ":
#        empty =[]
#     context = {"qs":hustle,"latest":latest,"category_count":category_count,"pagination":page_obj}

#     return render(request,"search.html",context)

import datetime
def home(request):   
    # print(datetime.timezone(now))  
    form=MyCustomLoginForm(request.POST or None)
    if form.is_valid():
        messages.error(request,"invalid password")    
    try:    
        the_id=request.COOKIES["device"]
        print(request.COOKIES["device"])
    except:       
        pass    
    context={"form":form}  
    return render(request,"home.html",context)      
     
def list(request):
    # product=requests.get("https://fakestoreapi.com/products").json()  

    form=MyCustomLoginForm(request.POST or None)
    filter=ColorFilter(data=request.GET)      
    try:       
        the_id=request.COOKIES["device"]    
        if request.user.is_authenticated:
            list=WishList.objects.filter(device=the_id)
            order=Order.objects.filter(device=the_id,ordered=False)
            if list.exists():
               wish_list=WishList.objects.get(device=the_id)
               wish_list.user=request.user
               wish_list.save() 
            if order.exists():
                my_order=Order.objects.get(device=the_id,ordered=False)   
                my_order.user=request.user
                my_order.save()    
              
        context={"wishlist":wish_list,"form":form}  
    except:        
        pass   
    product=Product.objects.all()
    category=Category.objects.all() 
    brand=Brands.objects.all()        
    color=Colors.objects.all()
    paginator=Paginator(product,9)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    context = {"products":page_obj,"categories":category,"brands":brand,"colors":color,"form":form,"filter":filter}
    return render(request,"shop-list.html",context)
    
def product(request,id):
    form=MyCustomLoginForm(request.POST or None)
    product=get_object_or_404(Product,id=id)
  
    # same=product.category
    same_product=Product.objects.filter(category=product.category)[0:3]
    views=Product.objects.all().order_by("-views")[0:3]
    product.views+=1     
    product.save()  
    category=Category.objects.all()
  
    brand=Brands.objects.all()      
    color=Colors.objects.all()            
    try:
        product=get_object_or_404(Product,id=id)
        the_id=request.COOKIES["device"]  
        if request.user.is_authenticated:
            for i in OrderProduct.objects.filter(device=the_id,ordered=False):
                i.user=request.user    
                i.save()   

            orders=OrderProduct.objects.filter(user=request.user,ordered=False)
            for d in orders:
                d.device=the_id
                devices=d
                d.save()
                # print(devices)
                    
            my_order=Order.objects.filter(device=the_id,ordered=False) 
            for a in my_order:
                a.user=request.user
                a.save() 
                users=a
                
            my_orders=Order.objects.filter(user=request.user,ordered=False)
            if my_orders.exists(): 
                for f in Order.objects.filter(user=request.user,ordered=False):   
                    f.items.add(devices)
                    f.save()
                    f.device=the_id
                    f.save()
                    
            if len(my_orders) != 1:
                my_deleted=Order.objects.filter(user=request.user,device=the_id,ordered=False)
                for c in my_deleted[1:]:
                    c.delete() 
                   
            if WishList.objects.filter(device=the_id).exists():
                wish_list=WishList.objects.get(device=the_id)
                wish_list.user=request.user
                wish_list.save()   
                print("wish")       
            list=WishList.objects.filter(user=request.user)
            for i in list:  
                i.device=the_id
                i.save()       
                print("here")
            if len(list) != 1:
                print("!+")
                my_deleted_list=WishList.objects.filter(user=request.user,device=the_id)
                for l in my_deleted_list[1:]:
                    l.delete() 

        context={"wishlist":wish_list,"same":same_product,"views":views,"products":product,"categories":category,"brands":brand,"colors":color,"form":form}
    except:
        try: #this is for wish_list cotenxt in COOKIES mode
            the_id=request.COOKIES["device"]
            wish_list=WishList.objects.get(device=the_id)
            context={"wishlist":wish_list,"products":product,"views":views,"same":same_product,"categories":category,"brands":brand,"colors":color,"form":form}
        except:
            context={"products":product,"same":same_product,"views":views,"categories":category,"brands":brand,"colors":color,"form":form}
            pass
        pass 

    # category_count=get_category_count()

    return render(request,"shop-detail.html",context)
   
def product_add(request,id): 
    product=get_object_or_404(Product,id=id)
    print(product)
    the_id=request.COOKIES["device"]
    
    if request.user.is_authenticated: 
        my_product=OrderProduct.objects.filter(item=product,user=request.user,ordered=False)
        if my_product.exists():
            messages.success(request,"you already have this order")
           
        else:
            plus_product=OrderProduct.objects.create(user=request.user,device=the_id,item=product)
            my_order=Order.objects.filter(user=request.user,ordered=False)
            if my_order.exists():
                for i in my_order:   
                    i.items.add(plus_product)
                    i.items.device=the_id
                    i.save()  
                    messages.success(request,"added to your cart")

            else:   
                order=Order.objects.create(user=request.user,device=the_id)
                this_order=Order.objects.filter(user=request.user,device=the_id,ordered=False)
                for i in this_order:
                    i.items.add(plus_product)  
                    i.save()     
                    messages.success(request,"added to your cart")
    else:
        plus_product=OrderProduct.objects.filter(device=the_id,item=product,ordered=False)
        if plus_product.exists():
            messages.success(request,"you already have this product")
        else:     
            my_product=OrderProduct.objects.create(item=product,device=the_id)
            this_order=Order.objects.filter(device=the_id,ordered=False)
            if this_order.exists():     
                for i in this_order:    
                    i.items.add(my_product)  
                    messages.success(request,"added to your cart")
            else:
                my_order=Order.objects.create(device=the_id)
                this_order=Order.objects.filter(device=the_id,ordered=False)
                for i in this_order:
                    i.items.add(my_product)     
                    messages.success(request,"added to your cart")
    return redirect(reverse("shop:product",kwargs={"id":id}))
    context = {}
    return render(request,"shop-detail.html",context)    

def wishlist(request):  
    form=MyCustomLoginForm(request.POST or None)
    try:
        the_id=request.COOKIES["device"]
        if request.user.is_authenticated:
            my_list=WishList.objects.filter(device=the_id)
        
            for i in my_list:
                i.user=request.user
                i.save() 
            for l in WishList.objects.filter(user=request.user):
               
                l.device=the_id
                l.save()  
            if len(WishList.objects.filter(user=request.user)) != 1:
                print("!+")
                my_deleted_list=WishList.objects.filter(user=request.user,device=the_id)
                for l in my_deleted_list[1:]:  
                    l.delete() 
            wish_list=WishList.objects.get(user=request.user)

        else:
            list=WishList.objects.filter(device=the_id)
            if list.exists:
                wish_list=WishList.objects.get(device=the_id)
                # print("authenticated")
     
        context={"wishlist":wish_list,"form":form}
    except:      
        pass
      
        context={"wishlist":False,"message":"you dont have list yet","form":form}
    return render(request,"customer-wishlist.html",context)

def wishlist_add(request,id):
    product=get_object_or_404(Product,id=id)
    try:
        the_id=request.COOKIES["device"]  
       
        # 
        if request.user.is_authenticated:
            my_list=WishList.objects.filter(user=request.user)
            # if request.is_ajax()
            if my_list.exists():
                for i in my_list:
                    i.item.add(product)   
                    i.devce=the_id
                    i.save()        
            else:
                list=WishList.objects.create(device=the_id,user=request.user)
                new_list=WishList.objects.filter(user=request.user)
                for i in new_list:
                    i.item.add(product)
                    
        else:    
            my_list=WishList.objects.filter(device=the_id)
            if my_list.exists(): 
                for i in my_list:
                    i.item.add(product)
                    i.device=the_id
                    i.save()
            else:
                my_list=WishList.objects.create(device=the_id)
                new_list=WishList.objects.filter(device=the_id)
                for i in new_list:
                    i.item.add(product)
                   
        return redirect(reverse("shop:product",kwargs={"id":id}))
    except:
       pass
    context = {}
    return render(request,"shop-detail.html",context)

def wishlist_remove(request,id):
    product=get_object_or_404(Product,id=id)
    try:
        the_id=request.COOKIES["device"]  
        if request.user.is_authenticated:
            my_list=WishList.objects.filter(user=request.user)
            if my_list.exists():
                for i in my_list:
                    i.item.remove(product)           
            else:
                pass
        else:
            my_list=WishList.objects.filter(device=the_id)
            if my_list.exists():
                for i in my_list:
                    i.item.remove(product)  
    except:
        pass   
    return redirect(reverse("shop:product",kwargs={"id":id}))
    context = {}
    return render(request,"shop-detail.html",context)  


def shop_basket(request):
    form=MyCustomLoginForm(request.POST or None)
    coupon_form=CouponForm(request.POST or None )
    coupon=Coupon.objects.all()
    try:     
        the_id=request.COOKIES["device"] 
        if request.user.is_authenticated:
            product=OrderProduct.objects.filter(device=the_id,ordered=False)
            if product.exists():
                for i in product: 
                    i.user=request.user
                    i.save()  
            a=OrderProduct.objects.filter(user=request.user,ordered=False)
            for b in a:
                b.device=the_id
                devices=b
                b.save()
            order=Order.objects.filter(device=the_id,ordered=False)  
            for d in order:
               d.user=request.user   
               d.save()
            orders=Order.objects.filter(user=request.user,ordered=False)
            for f in orders:
                f.items.add(devices)
                f.save()
                f.device=the_id
                f.save()
            if len(orders) != 1:
                my_deleted=Order.objects.filter(user=request.user,device=the_id,ordered=False)
                for c in my_deleted[1:]:
                    c.delete() 
            my_order=Order.objects.get(user=request.user,ordered=False)    
            list=WishList.objects.filter(device=the_id)
            if list.exists():   
               wish_list=WishList.objects.get(device=the_id)
               wish_list.user=request.user
               wish_list.save()
            same_product=OrderProduct.objects.filter(device=the_id,ordered=False)[0] #this is for same product in template
            same=Product.objects.filter(category=same_product.item.category)   
            context={"orders":my_order,"coupon_form":coupon_form,"products":same,"coupons":coupon}
        else:   
            my_orders=Order.objects.filter(device=the_id,ordered=False)
            print("HERE")
            if my_orders.exists():   
                
                my_order=Order.objects.get(device=the_id,ordered=False)  
            product=OrderProduct.objects.filter(device=the_id,ordered=False)[0]  
           
            same=Product.objects.filter(category=product.item.category) 
            context={"orders":my_order,"form":form,"coupon_form":coupon_form,"products":same,"coupons":coupon}    
    except:   
        context={"form":form,"coupon_form":coupon_form,"coupons":coupon}  
        pass  
    return render(request,"shop-basket.html",context)     

def coupon(request):      
    coupon_form=CouponForm(request.POST or None)  
    coupon=Coupon.objects.filter(name=request.POST.get("coupon"))  
    try:
        the_id=request.COOKIES["device"]   
        if coupon_form.is_valid():        
            if request.user.is_authenticated:    
                order=Order.objects.filter(user=request.user,device=the_id,ordered=False)
                if coupon.exists():
                    my_coupon=Coupon.objects.get(name=request.POST.get("coupon"))
                    if order.exists():
                        my_order=Order.objects.get(user=request.user,device=the_id,ordered=False)
                        if my_order.coupon is None:
                            my_order.coupon=my_coupon
                            my_order.save()          
                            messages.success(request,"coupon added suceessfully")   
                            pass   
                        else:
                            messages.error(request,"you alredy have this coupon")
                    else:
                        messages.error(request,"you should have order first")
                else:
                    messages.error(request,"invalid coupon")
            else:
                messages.error(request,"please sign in first")
            #     if not Order.objects.filter(user=request.user,device=the_id).exists():
            #         messages.error(request,"you dont have orders yet")
            #     if Order.objects.filter(user=request.user,device=the_id).exists():
            #         order=Order.objects.get(user=request.user,device=the_id)
            #         my_coupon=Coupon.objects.filter(name=request.POST.get("coupon"))  
            #         if my_coupon.exists():
            #             # my_coupon=Coupon.objects.filter(name=request.POST.get("coupon"))   
            #             for i in my_coupon: 
            #                 if order in i.orders.all() and request.user in i.user.all():         
            #                     messages.success(request,"expired coupon")
            #                 else:
            #                     i.orders.add(order)
            #                     i.user.add(request.user)
            #                     order.get_total_price()-100
            #                     order.save()
            #                     messages.success(request,"coupon added successfully")
            #                     return redirect(reverse("shop:orders"))
            #         else:
            #             messages.error(request,"invalid coupon")
            #             return redirect(reverse("shop:orders"))
                
            # else:
            #     messages.error(request,"please sign in to use this coupon")
            #     return redirect(reverse("shop:orders"))     
    except:
        pass
    context={"coupon_form":coupon_form,"coupons":coupon}
    return redirect(reverse("shop:orders"))     


def quantity_add(request,id):
    product=get_object_or_404(Product,id=id)
    try:
        the_id=request.COOKIES["device"] 
        order=OrderProduct.objects.get(item=product,device=the_id,ordered=False) 
        order.quantity +=1
        order.save()
    except:  
        pass
    return redirect(reverse("shop:orders"))

def quantity_remove(request,id):
    product=get_object_or_404(Product,id=id)
    # quantity=OrderProduct.objects.filter(user=request.user,item=product)
    # order=Order.objects.get(user=request.user,ordered=False)
    
    try:
        the_id=request.COOKIES["device"]
        # quantity=OrderProduct.objects.filter(user=request.user,item=product)
        order=Order.objects.get(device=the_id,ordered=False)
        quantity_remove=OrderProduct.objects.get(item=product,device=the_id,ordered=False)
        quantity_remove.quantity -=1
        quantity_remove.save() 
        if quantity_remove.quantity < 1:
            print("here")
            quantity_remove.delete()    
            # order.delete()
    except:
        pass    
    return redirect(reverse("shop:orders"))

def order_remove(request,id):
    product=get_object_or_404(Product,id=id)
    try:
        the_id=request.COOKIES["device"]
        if request.user.is_authenticated:
            my_product=OrderProduct.objects.get(user=request.user,item=product,ordered=False)
            order=Order.objects.get(user=request.user,ordered=False)
            my_product.delete()
            if order.coupon: 
               order.coupon =None
               order.save()
            return redirect(reverse("shop:orders"))
        else:
            my_product=OrderProduct.objects.get(device=the_id,item=product,ordered=False)
            order=Order.objects.get(device=the_id,ordered=False)
            my_product.delete()
            if order.coupon:
               order.coupon =None
               order.save()
    except:     
        pass    
        return redirect(reverse("shop:orders"))
    return redirect(reverse("shop:orders"))
                     
# class Customlogin(LoginView):
#     def get(self,request):
#         form=MyCustomLoginForm(request.POST or None)
#         context={"form":form}
#         return redirect(reverse("shop:home"))

class Customsignup(SignupView):     
    def get(self,request):
        form=MyCustomSignupForm(request.POST or None)
        login_form=MyCustomLoginForm(request.POST or None)
      
        context={"form":form,"login_form":login_form}
        return render(request,"customer-register.html",context)
    def post(self,request):
        form=MyCustomSignupForm(request.POST or None)
        login_form=MyCustomLoginForm(request.POST or None)
        if login_form.is_valid():
            print("valid")
        context={"form":form,"login_form":login_form}
      
        return render(request,"customer-register.html",context)   
"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

# This is your real test secret API key.
stripe.api_key ="sk_test_51IPqSdFPrf4ukXKcpnKL1CGg0CsRUgmF3drpQR5EZAogzbokQbWRNtcaTQDO0ULnbbANnN7eRC3alzigK3P0i1P4006nn4SKEp"
endpoint_secret="whsec_cayrLj4jD4w72C51ypJtsUbJkVs2dchV"

@login_required()
def create_checkout_session(request):
 
    YOUR_DOMAIN="https://universal-e-commerce.herokuapp.com/"         
    order=Order.objects.get(user=request.user,ordered=False)
    for i in order.items.all():
        items=i.quantity        
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        locale = "auto",

        shipping_address_collection={
        'allowed_countries': ['EG'],
        },
        # shipping_rates="null",
        line_items=[
            {       

                'price_data': {
                    'currency': 'EGP',
                    'unit_amount': int(order.get_total_price()*100), #cents
                    'product_data': {
                        'name':str(order.user),
                        'images': ['https://cdn.business2community.com/wp-content/uploads/2020/05/Ecommerce-marketing-trends.jpeg'],
                    },
                },
                'quantity': 1,  
            },
        ],
        metadata={      
        "order_id":order.id,
        "order":order, 
        },      
        mode='payment',
        success_url=YOUR_DOMAIN + 'success/',
        cancel_url=YOUR_DOMAIN + 'cancel/',
    )
    
    
    return JsonResponse({'id': checkout_session.id})


@csrf_exempt #this is to make post request is no longer need a csrf_toekn on this view
def my_webhook_view(request):
    payload = request.body
    print(payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header,settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:          
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)  
    # Handle the checkout.session.completed event 
  
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
      
        order=session["metadata"]["order"]
        my_order=Order.objects.get(id=order)
        my_order.ordered=True
        for i in my_order.items.all():
            i.ordered=True
            i.save()
        my_order.save()
       
        final=final_order.objects.get(order=my_order)
        final.customer_email=session["customer_details"]["email"]
        final.payment_intent=session["payment_intent"]
        final.city=session["shipping"]["address"]["city"]
        final.country=session["shipping"]["address"]["country"]
        final.line1=session["shipping"]["address"]["line1"]
        final.line2=session["shipping"]["address"]["line2"]
        final.postal_code=session["shipping"]["address"]["postal_code"]
        final.ordered=True
        final.save()
        send_mail(
            subject="completed payment",
            message=f"your payment completed successfully using {final.money}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[session["customer_details"]["email"]],
            fail_silently=False,       
                )
        messages.success(request,f"thank you for your trust, an email hass been sent to the E-mail provided in checkout form ({final.customer_email})")
    #    if event["type"] == "checkout.session.async_payment_failed"
    return HttpResponse(status=200)
        
   
@login_required()
def success(request):
    try:
        orders=Order.objects.filter(user=request.user,ordered=True).last()
        final=final_order.objects.get(order=orders)

    except:
        messages.success(request,"you dont have orders yet")
        return redirect(reverse("shop:home"))
    context={"orders":orders,"finals":final}
    return render(request,"success.html",context)        
@login_required()
def cancel(request):
    return render(request,"cancel.html")
   
@login_required()      
def payment(request):
    try:   
        order=Order.objects.get(user=request.user,ordered=False)
        form=OrderForm(request.POST or None)  
        empty=order.items.count()
        if empty == 0:
            messages.error(request,"you should have items in your list first")
            return redirect(reverse("shop:list"))
        if form.is_valid():    
            instance=form.save(commit=False)
            instance.name=request.user    
            money=order.get_total_price()
            order.price=money
            order.save()
            if final_order.objects.filter(name=request.user,order=order).exists():
                my_order=final_order.objects.get(order=order,name=request.user) 
                my_order.money=request.POST.get("money")
                my_order.save()     
                if instance.money == "PAYPAL" or instance.money == "CASH":
                    messages.success(request,"your order has been updated")
                    return redirect(reverse("shop:form"))
                else:
                    messages.success(request,"your order has been updated")
                    return redirect(reverse("shop:process"))
                    
            else:
                instance.order=order 
                instance.save()
                if instance.money == "PAYPAL" or instance.money == "CASH":
                    messages.success(request,"your order has been updated")
                    return redirect(reverse("shop:form"))
                else:
                    messages.success(request,"your order has been updated")
                    return redirect(reverse("shop:process"))
           
        context={"form":form,"orders":order}
    except:
        # pass
        messages.success(request,"you dont have orders yet")
        return redirect(reverse("shop:home"))
    return render(request,"payment.html",context) 
   
@login_required()
def form(request):
    try:
        orders=Order.objects.get(user=request.user,ordered=False,device=request.COOKIES["device"])
        my_order=final_order.objects.get(order=orders)
        form=OrderAddress(request.POST or None,instance=my_order)
        empty=orders.items.count()
        if empty == 0:
            messages.error(request,"you should have items in your list first")
            return redirect(reverse("shop:list"))
        if form.is_valid():
            form.save()
            return redirect(reverse("shop:process"))
        context={"form":form,"orders":orders,"final":my_order}
    except:
        messages.success(request,"you dont have orders yet")
        return redirect(reverse("shop:home"))
    return render(request,"shop-form.html",context)
@login_required()
def process(request):
    try:     
        orders=Order.objects.get(user=request.user,ordered=False,device=request.COOKIES["device"])
        my_order=final_order.objects.get(order=orders)
        empty=orders.items.count()
        if empty == 0:
            messages.error(request,"you should have items in your list first")
            return redirect(reverse("shop:list"))
        if request.method == "POST":
            if my_order.money == "CASH":
                for i in my_order.order.items.all():
                    i.ordered=True
                    i.save()  
                my_order.ordered = True
                orders.ordered = True
                orders.save()
                my_order.save() 
               
                messages.success(request,"thank you for using our service")
                return redirect(reverse("shop:success"))
        context={"orders":orders,"final":my_order}
    except:    
        messages.success(request,"you dont have orders yet")
        return redirect(reverse("shop:home"))
    return render(request,"shop-process.html",context)


from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import SandboxEnvironment,PayPalHttpClient
client_id="AUVCElDtljJUDVWukP9yrdedNic0J1B1XY1MtNfPhqxQU47F1F1A7C6ixKabvUCRZCTpkFihHBaTPR-F"
client_secret="ENepKuG3KheVNsthJjDS7B2amndWXWwaAQz3PJj8Ddi6O-QFQenD9frvveoUdGLrUdJUQ0DlzVap_b9Z"
# from paypalcheckoutsdk.orders import OrdersCreateRequest
@login_required()
def create(request,id):
    if request.method =="POST":
        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        client = PayPalHttpClient(environment)

        order= Order.objects.get(user=request.user,ordered=False)
        create_order = OrdersCreateRequest()
        #order            
        create_order.request_body (
            
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": order.converter(),
                            "breakdown": {
                                "item_total": {
                                    "currency_code": "USD",
                                    "value":  order.converter()
                                }
                                },
                            },                               


                    }
                ],      
                

            }     
        )
       
        # print()
        response = client.execute(create_order)
        data = response.result.__dict__['_dict']      
        return JsonResponse(data)
    else:
        return JsonResponse({'details': "invalide request"})
@login_required()
def capture(request,order_id,id):

    if request.method =="POST":
        capture_order = OrdersCaptureRequest(order_id)
        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        client = PayPalHttpClient(environment)
        response = client.execute(capture_order)
        data = response.result.__dict__['_dict']
       
        order=Order.objects.get(user=request.user,ordered=False,id=id)
        final=final_order.objects.get(name=request.user,order=order)      
        order.ordered=True
        for i in order.items.all():
            i.ordered=True  
            i.save()
        order.save()
        final.ordered=True
        final.payment_intent=data["id"]
        final.save() 
        send_mail(
        subject="completed payment",
        message=f"your payment completed successfully using {final.money}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[final.customer_email],
        fail_silently=False,       
            ) 
        return HttpResponseRedirect(reverse("shop:success"))
        messages.success(request,f"thanks for your trust, an email has been sent to your E-mail provided in checkout form ({final.customer_email})")   

    else:  
        messages.success(request,"you dont have orders yet")   
        return redirect(reverse("shop:home"))

    # body=json.loads(request.body)

    # return redirect(reverse("shop:home"))
@login_required()        
def history(request):
    order=final_order.objects.filter(name=request.user,ordered=True).order_by("-id")
    context={"orders":order}
    return render(request,"customer-orders.html",context)
     
@login_required()          
def history_details(request,id):
    try:
        order=final_order.objects.get(id=id)
    except:
        return redirect(reverse("shop:list"))
    context={"orders":order}
    return render(request,"customer-order.html",context)
     
def about(request):
    context={}
    return render(request,"about.html",context)
def packages(request):
    context={}
    return render(request,"packages.html",context)
def contact(request):
    form=ContactForm(request.POST or None)
    
    if form.is_valid():
        subject=form.cleaned_data.get("subject")
        message=form.cleaned_data.get("message")
        email=form.cleaned_data.get("email")
        send_mail(
            subject=subject,
            message=message + f' from {email}',
            from_email=email,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False, 
            auth_user=None,
            auth_password=None,
            connection=None,         
            html_message=None      
                )    
        
        messages.success(request,"thank you for youe Message,we will be in touch with you soon")
            return redirect(reverse("shop:contact"))
    context={"form":form}    
    return render(request,"contact.html",context)
# from django.shortcuts import render_to_response
from django.template import RequestContext

# HTTP Error 400
def my_custom_page_not_found_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response
  
    return response

def my_custom_error_view(request, template_name="404.html"):
    response = render(request,template_name)
    response.status_code = 500
    return response
     
    return response
def my_custom_permission_denied_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 403
    return response

    return response

def my_custom_bad_request_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 400
    return response
@login_required()
def customer(request):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        form=CustomerForm(request.POST or None,instance=request.user)
        user=User.objects.get(username=request.user)
        # custome_email=EmailAddress.objects.get(user=request.user)
        if form.is_valid():
            user.set_password(request.POST.get("confirm_password"))
            user.save()
            print(user.password)
            messages.success(request,"your password has been changed successfully")
            logout(request)
            return redirect(reverse("shop:home"))
        my_form=CustomerForm2(request.POST or None,instance=customer)
        if my_form.is_valid():
            user=request.user
            instance=my_form.save(commit=False)
            instance.save()
            messages.success(request,"information changed successfully")
            return redirect(reverse("shop:home"))

    else:        
        messages.success(request,"please login in first !")
    context={"customers":customer,"form":form,"my_form":my_form}
    return render(request,"customer-account.html",context)



# from amazon.api import AmazonAPI
#   SHOPIFY 
def shopify(request):
    products = requests.get("https://fakestoreapi.com/products").json()
  
    context={"products":products}
    return render(request,"shopify.html",context)
