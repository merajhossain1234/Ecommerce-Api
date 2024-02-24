
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, Category, Product, Cart, CartProduct, Order
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",'username','password','first_name','last_name','email')
        extra_kwargs = {'password':{'write_only':True,'required':True}}
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        Profile.objects.create(prouser=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['prouser']

    def validate(self,attrs):
        attrs['prouser'] = self.context['request'].user
        return attrs

    def to_representation(self,instance):
        response = super().to_representation(instance)
        response['prouser'] = UserSerializer(instance.prouser).data
        return response
        
 
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'date', 'category', 'image', 'market_price', 'selling_price', 'description']
        depth=1        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'date']
        
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'customer', 'total', 'completed', 'date']
        depth=1
        

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'price', 'quantity', 'subtotal']
        depth=1
        

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'cart', 'address', 'mobile', 'email', 'total', 'discount', 'order_status', 'date', 'payment']
        depth=1
        
