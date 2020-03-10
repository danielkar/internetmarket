from django.urls import path, include
from .views import product_list, product_detail, login, logout_view

app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product_list/<category_slug>', product_list, name='product_list_by_category'),
    path('<int:id>/<slug>', product_detail, name='product_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', login, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
]
