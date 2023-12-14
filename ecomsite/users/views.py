from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,UpdateView,DeleteView
from  django.contrib.auth.forms import  UserCreationForm ,UserChangeForm
from django.contrib import messages
from .models import Address
from shop.models import Order
from .forms import RegisterForm ,AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == "POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username}, your account is created')
            return redirect('login')
    else:

        form=RegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profilepage(request):
    address=Address.objects.filter(user=request.user)
    orders=Order.objects.get(user=request.user)
    items=orders.items
    return render (request,'users/profile.html',{'address':address,'orders':orders,'items':items})




class AddressCreateView(LoginRequiredMixin,CreateView):
    model=Address
    form_class=AddressForm
    template_name = 'users/address_form.html'
    success_url ='/profile/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect('profile')
    
class AddressUpdateView(UpdateView):
    model=Address
    fields='__all__'

class AddressDeleteView(DeleteView):
    model=Address
    success_url ='/profile/'
    
def edit_user(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'users/edit_user.html', {'form': form})