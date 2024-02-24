from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from .models import Product, Category,Profile,Cart,CartProduct,Order
from .serializers import ProductSerializer, CategorySerializer,ProfileSerializer,CartSerializer,CartProductSerializer,UserSerializer,OrderSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated




class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    lookup_field = "id"

    def retrieve(self, request, id=None):
        return super().retrieve(request)





class CategoryView(viewsets.ViewSet):
    def list(self, request):
        categories = Category.objects.all().order_by("-id")
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        category = Category.objects.get(id=pk)
        category_serializer = CategorySerializer(category)
        category_data = category_serializer.data
        
        all_data=[]

        category_products = Product.objects.filter(category_id=category_data['id'])
        category_products_serializer = ProductSerializer(category_products, many=True)
        category_data["category_products"] = category_products_serializer.data
        all_data.append(category_data)
        return Response(all_data)
  
  
  
    
class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return Response({"error": True, "message": "User is not authenticated"})

        try:
            # Query the profile using get_object_or_404
            queryset = get_object_or_404(Profile, prouser=self.request.user)
            serializer = ProfileSerializer(queryset)
            response_msg = {"error": False, "data": serializer.data}
        except:
            response_msg = {"error": True, "message": "Something is wrong"}

        return Response(response_msg)
            
class OrderViewset(viewsets.ViewSet):
    def list(self,request):
        query=Order.objects.filter(cart__customer=request.user.profile)
        serializers=OrderSerializer(query,many=True)
        all_data=[]
        for order in serializers.data:
            cartproduct=CartProduct.objects.get(cart_id=order['cart']['id'])
            cartproduct_serializer=CartProductSerializer(cartproduct,many=True)
            order["cartproduct"]=cartproduct_serializer.data
            all_data.append(order)
            
        return Response(all_data)
    
    
    def retrieve(self,request,pk=None):
        try:
            queryset=Order.objects.get(id=pk)
            serializers=OrderSerializer(queryset)
            data=serializers.data
            all_data=[]
            cartproduct=CartProduct.objects.filter(cart_id=data['cart']['id'])
            cartproduct_serailizer=CartProductSerializer(cartproduct,many=True)
            data["cartproduct"]=cartproduct_serailizer.data
            response_message={"error":False,"data":all_data}
        except:
            response_message={"error":True,"message":"Not found"}
            
        return Response(response_message)
    
    def create(self,request):
        cart_id=request.data["cartId"]
        cart_obj=Cart.objects.get(id=cart_id)
        address=request.data["address"]
        mobile=request.data["mobile"]
        email=request.data["email"]
        cart_obj.completed=True
        cart_obj.save()
        
        created_order=Order.objects.create(
            cart=cart_obj,
            address=address,
            mobile=mobile,
            email=email,
            total=cart_obj.total,
            discount=3
            
            
        )
        return Response({"message":"Order Received","cart id":cart_id,"order id":created_order.id})


    
class ProfileUpdate(APIView):
    def post(self,request):
        try:
            user=request.user
            data=request.data
            user_obj=User.objects.get(username=user)
            user_obj.first_name=data["first_name"]
            user_obj.last_name=data["last_name"]
            user_obj.email=data["email"]
            user_obj.save()
            response_mesg={"msg":"user is created"}
        except:
            response_mesg={"msg":"user is not  created"}  
        return Response(response_mesg)


   
#update image or profile updated   
class ProfileImageUpdate(APIView):
    def post(self,request):
        try:
            user=request.user
            data=request.data
            query=Profile.objects.get(prouser=user)
            serializers=ProfileSerializer(query,data=data,context={"request":request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            response_mesg={"msg":"profile image updated"}
        except:
          response_mesg={"msg":"profile image is not updated"}
        return Response(response_mesg)



class Mycart(viewsets.ViewSet):
    def list(self,request):
        query=Cart.objects.filter(customer=request.user.profile)
        serializers=CartSerializer(query,many=True)
        all_data=[]
        for cart in serializers.data:
            cart_product=CartProduct.objects.filter(cart=cart['id'])
            cart_product_serializer=CartProductSerializer(cart_product,many=True)
            cart["cartproduct"]=cart_product_serializer.data
            all_data.append(cart)
            
        return Response(all_data)
  
  
  
    
class RegisterView(APIView):
    def post(self,request):
        data=request.data
        serializers=UserSerializer(data)
        if serializers.is_valid():
            serializers.save()
            return Response({"errors":False,"message":f"success fully register","data":serializers.data})
        return Response ({"error":True,"message":"A user with that username already exists! Try Anather Username"})  




class AddtoCart(APIView):
    def post(self,request):
        product_id=request.data['id']
        product_obj=Product.objects.get(id=product_id)
        
        #finding is any cart is exist for this user
        cart_cart=Cart.objects.filter(customer=request.user.profile).filter(completed=False).first()
        
        cart_product_obj=CartProduct.objects.filter(product_id=product_id).first()
        
        try:
            #checking here
            if cart_cart:
                #if exist cart then finding this product at this cartproduct
                this_product_in_cart=cart_cart.cartproduct_set.filter(product=product_obj)
                
                if this_product_in_cart.exists():
                    #and if this product is exist at the cart then update the cart product details
                    cartproduct_uct=CartProduct.objects.filter(product=product_obj).filter(cart_completed=False).first()
                    cartproduct_uct.quantity+=1
                    cartproduct_uct.subtotal+=product_obj.selling_price
                    cartproduct_uct.save()
                    cart_cart.total+=product_obj.selling_price
                    cart_cart.save()
                    
                else:
                    #if cart exist but cart product not exist then create a cart-product with details and save it
                    cart_product_new=CartProduct.objects.create(cart=cart_cart,price=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price)
                    cart_product_new.product.add(product_obj)
                    cart_cart.total+=product_obj.selling_price
                    cart_cart.save()
                    
                    
            else:
                # if cart is not exist then create a cart and find new cart by the instance user which are not ordered 
                #and create a new cart-product whit details   and save cart and cart-product          
                Cart(customer=request.user.profile, total=0, completed=False)
                new_cart=Cart.objects.filter(customer=request.user.profile).filter(completed=False).first()
                cart_product_new=CartProduct.objects.create(cart=new_cart,price=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price)
                cart_product_new.product.add(product_obj)
                
                new_cart.total+=product_obj.selling_price
                new_cart.save()
                
            response_mesage = {'error':False,'message':"Product add to card successfully","productid":product_id}
                
                
        except:
            response_mesage = {'error':True,'message':"Product Not add!Somthing is Wromg"}
            
            
        return Response(response_mesage) 
            
                
class UpdateCartProduct(APIView):
    def post(self, request, *args, **kwargs):
        cart_product_object=CartProduct.objects.get(id=request.data['id'])
        cart_of_cart_product_object=cart_product_object.cart
        
        
        cart_product_object.quantity+=1
        cart_product_object.subtotal+=cart_product_object.price
        cart_product_object.save()
        
        cart_of_cart_product_object.total+=cart_product_object.price
        cart_of_cart_product_object.save()
        
        
        return Response({"message":"CartProduct Add Update","product":request.data['id']})
        
        
class EditCartProduct(APIView):
    def post(self,request,*args, **kwargs):
        cart_product_object=CartProduct.objects.get(id=request.data['id'])
        cart_of_cart_product_object=cart_product_object.cart
        
        
        cart_product_object.quantity-=1
        cart_product_object.subtotal-=1
        cart_product_object.save()
        
        
        
        cart_of_cart_product_object.total-=cart_product_object.price
        cart_of_cart_product_object.save()
        
        if(cart_product_object.quantity==0):
            cart_product_object.delete()
            
        return Response({"message":"CartProduct Add Update","product":request.data['id']})
        
        
        
class Deletecartproduct(APIView):
    def post(self,request):
        CartProduct.objects.filter(id=request.data["id"]).delete()
        return Response({"msg":"deleted succesfully"})
 
    
    
    
class DeleteFullCart(APIView):
    def post(self,request):
        try:
            card_obj = Cart.objects.get(id=request.data['id'])
            card_obj.delete()
            responsemessage = {"message":"Cart Delated"}
        except:
            responsemessage = {"message":"Somthing is wrong"}
        return Response(responsemessage)
        