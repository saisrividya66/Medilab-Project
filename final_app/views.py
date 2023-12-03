from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from  django.contrib.auth.models import User
from  django.contrib.auth import authenticate,login,logout
from final_app.models import product,Cart,Order
from django.db.models import Q
import random
import razorpay

from django.core.mail import send_mail

# Create your views here.
def func1(request):
    return HttpResponse("This is a first function")
def func2(request):
    return HttpResponse("This is a second function")
def func3(request):
    return HttpResponse("This is a Third function")
def func4(request):
    return HttpResponse("This is a Fourth function")



def edit(request,rid):
    print("id to be edited:",rid)
    return HttpResponse("id to be edited:"+rid)
def add(request,a,b):
    res=int(a)+int(b)
    print("result:",res)
    return HttpResponse("resut:"+str(res))
class SimpleView(View):
    def get(self,request):
        return HttpResponse("Simple View")
def hello(request):
    context={}
    context['products']=[{'id':1,'name':'Vidya'},
    {'id':2,'name':'Vidya'},
    {'id':5,'name':'Vidya'}]
 
   
    context['l']=[10,20,30,40,50]
   
    return render(request,'hello.html',context)

def home(request):
    #userid=request.user.id
    #print("id of logged in user:",userid)
   # print("Result is:",request.user.is_authenticated)
   context={}
   p=product.objects.order_by('price')
   context['products']=p
   print(p)




   return render(request,'index.html',context)
 

def product_details(request,pid):
    p=product.objects.filter(id=pid)
    context={}
    context['products']=p
    return render(request,'product_details.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be empty"
            return render(request,'register.html',context)
        elif upass != ucpass:
               context['errmsg']="password and confirm password didnot matched"
               return render(request,'register.html',context)

         
        else:
            try:
                 u=User.objects.create(password=upass,username=uname,email=uname)
                 u.set_password(upass)
                 u.save()
                 context['success']="User Created Successfully"
                 return render(request,'register.html',context)
             #return HttpResponse("User Created Successfully")
            except Exception:
                context['errmsg']="User name already existed"
                return render(request,'register.html',context)
       
            
    else:
        return render(request,'register.html')

         

      
def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def user_login(request):
        if request.method=="POST":
             uname=request.POST['uname']
             upass=request.POST['upass']
            
             context={}
             if uname=="" or upass=="":
                 context['errmsg']="Fields cannot be empty"
                 return render(request,'login.html',context)
             else:
                u=authenticate(username=uname,password=upass)
                print(u)
                #print(u.username)
                #print(u.password)
                if u is not None:
                    login(request,u)
                    return redirect('/home')
                else: 
                    context['errmsg']="Invalid username and password"
                    return render(request,'login.html',context)
               


           
                return HttpResponse("Data fetched Successfully")
              
        else:
            return render(request,'login.html')

    
    

            
                        
                
            
           
def user_logout(request):
    logout(request)
    return redirect('/home')


def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv== '0':
        col='price'
    else:
        col='-price'
   # p=product.objects.order_by(col)
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    print(min)
    print(max)
    #return HttpResponse("value fetched")
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
         userid=request.user.id
         print(userid)
         print(pid)
         u=User.objects.filter(id=userid)
         print(u[0])
         p=product.objects.filter(id=pid)
         print(p[0])
         q1=Q(uid=u[0])
         q2=Q(pid=p[0])
         context={}
         context['products']=p
         c=Cart.objects.filter(q1 & q2)
         n=len(c)
         if n == 1:
            context['msg']="product already existed"
            return render(request,'product_details.html',context)
                 
     
         else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
      
            context['success']="Product Added to cart"
            return render(request,'product_details.html',context)
            return HttpResponse("products added")

         
    

   
    
    
       

    else:
        return redirect('/login')
      

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c)
    #print(c[0])

    #print(c[0].pid)
    #print(c[0].uid)
    
    #print(c[0].pid.name)
    #print(c[0].pid.price)
    #print(c[0].uid.is_superuser)
    np=len(c)
    print(np)
    s=0
    for x in c:
        s=s+x.pid.price
    print(s)
    context={}
    context['total']=s
    context['data']=c
    context['n']=np


    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()

    return redirect('/viewcart')


def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    #print(c)
    #print(c[0])
    #print(c[0].qty)


    if qv == '1':
        t=c[0].qty +1
        c.update(qty=t)

    
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
            
    return redirect("/viewcart")
  

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        print(x)
        print(x.uid)
        print(x.pid)
        print(x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    context={}
    context['data']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        context['total']=s
        context['n']=np



        #print(x)
        #print(x.uid)
        #print(x.pid)
        #pr[int(x.qty)

    return render(request,'placeorder.html',context)



def makepayment(request):
    uemail=request.user.username
    print(uemail)
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_40WZydykyBdyZ0", "kEiWEENN2qF9ypdvkQ8Xjsap"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    #print(payment)
    #return HttpResponse("succe")
    context={}
    context['data']=payment
    uemail=request.user.username
    print(uemail)
    context['uemail']=uemail
    return render(request,'pay.html',context)


def sendusermail(request,uemail):
    #uemail=request.user.username
    #print(uemail)
    msg="order details are:"
    send_mail(
        "Medilab has greanted ur order and medicines Placed Successfully",
        msg,
        "cherukumudisaisrividhya@gmail.com",
        [uemail],
        fail_silently=False,
    )

    
    return HttpResponse("USERMAIL")
   