from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name=""),
    # path('register', views.register, name="register"),
    # path('my-login', views.my_login, name="my-login"),
    # path('user-logout', views.user_logout, name="user-logout"),
    path('', views.dashboard, name="dashboard"),
    path('about-us', views.about_us, name="about-us"),
    path('contact/', views.contact, name='contact'),
    path('shop', views.shop, name='shop'),
    path('seedling_list', views.seedling_list, name='seedling_list'),
    path('<int:pk>/', views.seedling_detail, name='seedling_detail'),
    # path('add-to-cart/<int:seedling_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
]