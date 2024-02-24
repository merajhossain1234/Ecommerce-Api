
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('allproduct/',ProductListView.as_view(),name="products"),
    #get single product
    path('allproduct/<int:pk>/',ProductListView.as_view(),name="product"),
    path('categories/',CategoryView.as_view({'get': 'list'}),name="categories"),
    #cateory with all products
    path('categories/<int:pk>/',CategoryView.as_view({'get': 'retrieve'}),name="category_with_products"),
    
    #user profile View
    path('profile/',ProfileView.as_view(),name='profile_of_user'),
    path('profileupdate/',ProfileUpdate.as_view(),name='profile_update_of_user'),
    path('profileimageupdate/',ProfileImageUpdate.as_view(),name='profile_image_of_user_user'),
    
    #AddtoCart
    path('AddtoCart/',AddtoCart.as_view(),name='Add_to_Cart'),
    path("mycart/",Mycart.as_view({'get': 'list'}),name="my_cart"),
    path("orderviewandcreate/",OrderViewset.as_view({'get': 'list'}),name="OrderViewset"),
    
    path("updatecartproduct/",UpdateCartProduct.as_view(),name="updatecartproduct"),
    path("editcartproduct/",EditCartProduct.as_view(),name="editcartproduct"),
    path("deletecartproduct/",Deletecartproduct.as_view(),name="delatecartproduct"),
    path("deletefullcart/",DeleteFullCart.as_view(),name="delatefullcart"),
    
    
    
]
