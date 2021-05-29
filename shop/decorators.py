 
from .models import *
def user_session(function):
    def wrap(request, *args, **kwargs):
        try:   
            the_id=request.COOKIES["device"]
            print(request.COOKIES["device"])
            customer,created=Customer.objects.get_or_create(device=the_id)
            wish_list,created=WishList.objects.get_or_create(device=the_id)
            if request.user.is_authenticated:
                print("here")
                customer.user=request.user
                wish_list.user=request.user
                customer.save()
                wish_list.save()
                wish_list,created=WishList.objects.get_or_create(device=the_id)
                if wish_list.exists:
                    print("done")   
            else:
                print("list here")
            context={"wishlist":wish_list}
                # customer=Customer.objects.get_or_create(device=the_id)
                # if not wish_list.exists:    
        except: 
            print("passed") 
            pass
            context={"list":True}
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap