from django.urls import path
from . import views
from .views import *
   
app_name="shop" 
urlpatterns = [
    path("",views.home,name="home"),
    path("list/",views.list,name="list"),
    path("detail/<str:id>",views.product,name="product"),
    path("add-product/<str:id>",views.product_add,name="add_product"),
    path("wishlist/",views.wishlist,name="wishlist"),
    path("add-wishlist/<str:id>/",views.wishlist_add,name="add_wishlist"),
    path("remove-wishlist/<str:id>/",views.wishlist_remove,name="remove_wishlist"),
    path("orders/",views.shop_basket,name="orders"),
    path("orders-add/<str:id>",views.quantity_add,name="quantity_add"),
    path("orders-minus/<str:id>",views.quantity_remove,name="quantity_remove"),
    path("order-remove/<str:id>",views.order_remove,name="order_remove"),
    path("coupons/",views.coupon,name="coupon"),
    path("history/",views.history,name="history"),
    path("history/order/<str:id>/",views.history_details,name="order_detail"),
    path("about-us/",views.about,name="about"),
    path("pakages/",views.packages,name="package"),   
    path("contact-us/",views.contact,name="contact"),
    path("my-profile/",views.customer,name="profile"),

    path("shopify/",views.shopify,name="shopify"),

#    path("login/",Customlogin.as_view(),name="login"),
    # path("register/",Customsignup.as_view(),name="signup"),
         
   path("checkout-session/",views.create_checkout_session,name="session"),     
  path("webhook/",views.my_webhook_view,name="webhook_stripe"),       


   path("success/",views.success,name="success"),  
    path("cancel/",views.cancel,name="cancel"),  
    path("payment/",views.payment,name="payment"),
    path("payment/form/",views.form,name="form"),
    path("process/",views.process,name="process"),
    path("create/<id>/",views.create,name="create"),  
    path("capture/<str:order_id>/<str:id>/",views.capture,name="capture"),  
]
                 