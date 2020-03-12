from django.urls import path, include
from .views import product_list, product_detail, register, user_login, index

app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product_list/<category_slug>', product_list, name='product_list_by_category'),
    path('<int:id>/<slug>', product_detail, name='product_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('user_login/', user_login, name='user_login'),
    path('index/', index, name='index'),
]
