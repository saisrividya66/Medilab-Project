"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from final_app import views
from django.conf.urls.static import static
from final import settings




urlpatterns = [
  
    path('func1',views.func1),
    path('func2',views.func2),
    path('func3',views.func3),
    path('func4',views.func4),
    path('edit/<rid>',views.edit),
      path('add/<a>/<b>',views.add),
      path('simpleview',views.SimpleView.as_view()),
    path('hello',views.hello),
    path('home',views.home),
     path('pdetails/<pid>',views.product_details),
      path('register',views.register),
      path('about',views.about),
      path('contact',views.contact),
      path('login',views.user_login),
      path('logout',views.user_logout),
      path('catfilter/<cv>',views.catfilter),
      path('sort/<sv>',views.sort),
      path('range',views.range),
      path('addtocart/<pid>',views.addtocart),
      path('viewcart',views.viewcart),
      path('remove/<cid>',views.remove),
       path('updateqty/<qv>/<cid>',views.updateqty),
      path('placeorder',views.placeorder),
      path('makepayment',views.makepayment),
      path('sendmail/<uemail>',views.sendusermail)


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)