from django.shortcuts import render, get_object_or_404
from .models import Category, Product, User
from django.contrib.auth import authenticate, login, logout

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


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('base')
        else:
            messages.error(request,'username or password not correct')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('base')