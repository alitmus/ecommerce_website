from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

class Category(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='categories/',blank=True,null=True)

    def __str__(self) :
        return self.name
    class Meta:
        verbose_name_plural='Categories'


class Product(models.Model):
    group_choices=[
        ('w','Women'),
        ('m','Men'),
        ('k','Kids'),]
    label_choices=[
        ('warning','new'),
        ('danger','sale'),
        ('info','bestseller'),
        ('success','season'),
        ]
    
    title=models.CharField(max_length=200)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.RESTRICT)
    label=models.CharField(max_length=9,choices=label_choices)
    group=models.CharField(max_length=1,choices=group_choices,null=True)
    description=models.CharField(max_length=300,default=f'{title} for {group}')
    image=models.ImageField(upload_to='products/',default='default-product.jpg')

    def __str__(self) :
        return f'{self.title} of {self.group} for {self.price} $'
    
    def get_add_to_cart_url(self):
        return reverse("shop:add_to_cart",kwargs={'pk':self.pk})
    
    def get_remove_from_cart_url(self):
        return reverse("shop:remove_from_cart",kwargs={'pk':self.pk})
    
    def get_increase_quantity_url(self):
        return reverse("shop:increase_quantity",kwargs={'pk':self.pk})
    

class OrderItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)     
    item=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price()-self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()


class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()   
    ordered=models.BooleanField(default=False)     

    def __str__(self):
        return self.ordered_date

    def get_total(self):
        total=0
        for order_item in self.items.all():
            total +=order_item.get_final_price()
        return total    


class Image(models.Model):
    name = models.CharField(max_length=200 )
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,related_name='images')
    image = models.ImageField(upload_to='products/',default='default-product.jpg')

    def __str__(self):
        return self.product.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)
    content = models.TextField()
    rating = models.IntegerField(
        
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return f"{self.user} said :{self.title} about :{self.product.title} "    
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email