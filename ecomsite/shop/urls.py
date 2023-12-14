from django.urls import path
from .views import (index ,ProductCreateView,product_detail,
                    about_view,women_view,men_view,kids_view,add_to_cart,CheckoutView,remove_from_cart,increase_quantity,
                    OrderView
                    )

app_name='shop'

urlpatterns=[
    path('',index,name='index'),
    path('product_form/',ProductCreateView.as_view(),name='product_form'),
    path('product/<int:pk>/',product_detail,name='product'),
    path('about/',about_view,name='about'),   
    path('women/',women_view,name='women'),
    path('men/',men_view,name='men'),
    path('kids/',kids_view,name='kids'),
    path('add_to_cart/<int:pk>',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:pk>',remove_from_cart,name='remove_from_cart'),
    path('increase_quantity/<int:pk>',increase_quantity,name='increase_quantity'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('order/',OrderView.as_view(),name='order'),
]