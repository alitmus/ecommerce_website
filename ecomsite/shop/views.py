from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Product , Review ,Order ,OrderItem ,Category
from django.core.paginator import Paginator
from django.views.generic import CreateView,View
from .forms import ReviewForm ,SubscriberForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from users.models import User ,Address
from django.utils import timezone
from django.contrib import messages


def index(request):
    products=Product.objects.all()
    item_name = request.GET.get('item_name')
    categories=Category.objects.all()

    if item_name != "" and item_name is not None:
       products=products.filter(title__icontains=item_name)

    paginator=Paginator(products,6)
    page = request.GET.get('page')
    products=paginator.get_page(page)
    return render(request,'shop/index.html',{'products':products,'categories':categories})



def product_detail(request, pk):
    active_user = request.user
    product = Product.objects.get(id=pk)
    reviews = Review.objects.filter(product=product)

    sum_rating=sum(review.rating for review in reviews)
    num_rating=len(reviews)
    avg_rating=round(sum_rating/num_rating if num_rating > 0 else 0,1)
    avg_percentage=avg_rating * 100 / 5

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = active_user
            review.product = product
            review.save()
            form = ReviewForm()
            return HttpResponseRedirect(request.path_info)
       
    else:
            form = ReviewForm()
    
 
    return render(request, 'shop/product.html', {'product': product, 'reviews': reviews,'form': form,'avg_rating':avg_rating,'avg_percentage':avg_percentage,})    


def add_to_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            messages.info(request,'This item is in your cart.')
                                                      
        else:
            messages.info(request,'This item is added to your cart.')
            order.items.add(order_item)

    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,'This item is added to your cart')
        return redirect(reverse('shop:product',args=[item.pk]) )

    return redirect(reverse('shop:product',args=[item.pk]) )


def increase_quantity(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    order=order_qs[0]
    order_item.quantity +=1
    order_item.save()
    messages.info(request,'This item quantity is increased.')
    return redirect('shop:checkout')
                                                        
       

def remove_from_cart(request,pk):
    item=get_object_or_404(Product,pk=pk)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item=OrderItem.objects.filter(
                item=item, 
                user=request.user,
                ordered=False
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request,'This item quantity is decreased.')
                return redirect("shop:checkout")
            else :    
                order.items.remove(order_item)
            messages.info(request,'This item is removed from your cart.')
            return redirect("shop:checkout")

        else:
            messages.info(request,'This item is not in your cart.')
            return redirect("shop:checkout")
    else:
        messages.info(request,'You do not have an active order.')
        return redirect("shop:checkout")



class CheckoutView(View):
    def get (self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            address=Address.objects.filter(user=self.request.user)

            context={
                'object':order,'address':address
            }
            return render(self.request,'shop/checkout.html',context=context)

        except ObjectDoesNotExist:
            messages.error(self.request,'You dont have any order')
            return redirect('/')
        
    def update_quantity_item(self, pk):
        order_item = get_object_or_404(OrderItem, id=pk)
        if self.request.method == "POST":
            order_item.quantity += 1
            order_item.save()
        if self.request.method == "POST":   
            order_item.quantity -= 1
            order_item.save()



class OrderView(View):
    def get (self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            items=order.items
            context={
                'object':order,'items':items
            }
            return render(self.request,'shop/order.html',context=context)

        except ObjectDoesNotExist:
            messages.error(self.request,'You dont have any order')
            return redirect('/')
    

def about_view(request):
    context={
        'products_count':Product.objects.all().count,
        'customers':User.objects.all().count,
    }
    return render(request,'shop/about.html',context=context)


def women_view(request):

    products=Product.objects.filter(group='w')
    context={
        'products':products
    }
    return render (request,'shop/women.html',context=context)
def men_view(request):

    products=Product.objects.filter(group='m')
    context={
        'products':products
    }
    return render (request,'shop/men.html',context=context)
def kids_view(request):

    products=Product.objects.filter(group='k')
    context={
        'products':products
    }
    return render (request,'shop/kids.html',context=context)


class ProductCreateView(CreateView):
    model =Product 
    fields='__all__'
    success_url='/shop/product/'
    

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:index')  
    else:
        form = SubscriberForm()
    return render(request, 'ebase.html', {'subscribe': form})