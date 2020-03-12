from django.shortcuts import render, get_object_or_404
from .models import Category, Product, User
from django.contrib.auth import authenticate, login, logout
from shop.forms import UserForm,UserProfileInfoForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def product_list(request, category_slug=None):
	num_customers = User.objects.count()
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	context={
		'num_customers': num_customers,
		'num_visits': num_visits,
		'category': category,
		'categories': categories,
		'products': products,
	}
	return render(request, 'shop/product/list.html', context)

def product_detail(request, id, slug):
	product = get_object_or_404(Product,
								id=id,
								slug=slug,
								available=True)
	context={
		'product': product,
	}
	return render(request, 'shop/product/detail.html', context)

def index(request):
    return render(request,'shop/base.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('base'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        print(user_form, profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration/registration.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('base'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'registration/login.html', {})