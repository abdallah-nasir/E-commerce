from django import forms 
from .models import *
from allauth.account.forms import LoginForm,SignupForm



class MyCustomLoginForm(LoginForm):
    
    def login(self, *args, **kwargs):
    
        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)


class MyCustomSignupForm(SignupForm):
    
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
class CouponForm(forms.ModelForm):
    coupon=forms.CharField(max_length=50)
    class Meta:
        model=Coupon
        fields=["coupon"]

    # def clean_coupon(self):
    #     my_coupon=self.cleaned_data["coupon"]
    #     # order=Order.objects.filter(user=self.instance.user,ordered=False)
    #     if Coupon.objects.filter(user=self.instance.user,orders=self.instance).exists():
    #         raise forms.ValidationError("you already used this coupon")
    #     if not Coupon.objects.filter(name__iexact=my_coupon).exists():
    #         raise forms.ValidationError("invalid coupon")
    #     return my_coupon 
class CouponForm(forms.ModelForm):
    coupon=forms.CharField(max_length=50)
    class Meta:
        model=Coupon
        fields=["coupon"]
        
   
CHOICES=(
    ("PAYPAL","PAYPAL"),
    ("VISA / MASTERCARD","VISA / MASTERCARD"),
    ("CASH","CASH")
)
class OrderForm(forms.ModelForm):
    money=forms.ChoiceField(label="pay with",choices=CHOICES)
    class Meta:
        model=final_order
        fields=["money"]
        
    
        
class OrderAddress(forms.ModelForm):
    customer_email=forms.EmailField(max_length=100)
    city=forms.CharField(max_length=50)
    country=forms.CharField(max_length=50)
    line1=forms.CharField(max_length=100)
    line2=forms.CharField(max_length=100)
    postal_code=forms.CharField(max_length=7)
    class Meta:
        model=final_order
        fields="__all__"
        exclude=["name","order","money","ordered","payment_intent","status"]
        
        
class ContactForm(forms.Form):
    first_name=forms.CharField(max_length=20)
    last_name=forms.CharField(max_length=20)
    email=forms.EmailField()
    subject=forms.CharField(max_length=50)
    message=forms.CharField(max_length=200)

class CustomerForm(forms.ModelForm):
    password=forms.CharField(label="old password",widget=forms.PasswordInput())
    new_password=forms.CharField(label="new password",widget=forms.PasswordInput())
    confirm_password=forms.CharField(label="confirm password",widget=forms.PasswordInput())
    class Meta:    
        model=User
        fields=["password"]


            
    def clean_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('password')
        user=User.objects.get(username=self.instance.username)
        if user.check_password(old_password) == False:
            raise forms.ValidationError("The old password that you have entered is wrong.")
        return old_password

    def clean_confirm_password(self,*args,**kwargs):
        new_password=self.cleaned_data.get("new_password")
        user=User.objects.get(username=self.instance.username)
        confirm_password=self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("password dosen't match")
        if user.check_password(confirm_password) == True:
            raise forms.ValidationError("you have entered an old password")
        return confirm_password
    
    
class CustomerForm2(forms.ModelForm):
    class Meta:    
        model=Customer
        fields="__all__"
        exclude=["user"]

