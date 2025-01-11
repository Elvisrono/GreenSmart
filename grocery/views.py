from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient

from grocery.forms import CreateUserForm, LoginForm
from grocery.models import ContactMessage, Seedling, CartItem
from django.http import JsonResponse
from .models import CartItem
import json
from .cart import Cart


# Create your views here.
def home(request):

    return render(request, 'index.html')

# def register(request):
#
#     form = CreateUserForm()
#
#     if request.method == "POST":
#
#         form = CreateUserForm(request.POST)
#
#         if form.is_valid():
#
#             form.save()
#
#             messages.success(request, "Account created successfully!")
#
#             return redirect("my-login")
#
#     context = {'form':form}
#
#     return render(request, 'register.html', context=context)

def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Make sure you're using .get(), not ()
        subject = request.POST.get('subject')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Save the data to the database
        contact_message = ContactMessage(
            email=email,
            subject=subject,
            phone_number=phone_number,
            message=message
        )
        contact_message.save()

        messages.success(request, "Message has been sent successfully!")

    return render(request, 'about-us.html')


# def my_login(request):
#     form = LoginForm()
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 return redirect("dashboard")
#     context = {'form': form}
#     return render(request, 'my-login.html', context=context)

# @login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'dashboard.html')

def about_us(request):
    return render(request, 'about-us.html')

def shop(request):
    return render(request, 'shop.html')

def user_logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("my-login")


# views for the sedling
def seedling_list(request):
    seedlings = Seedling.objects.all()
    return render(request, 'seedling_list.html', {'seedlings': seedlings})


def seedling_detail(request, pk):
    seedling = get_object_or_404(Seedling, pk=pk)
    return render(request, 'seedling_detail.html', {'seedling': seedling})


def add_to_cart(request, item_id):
    # Check if the request is a POST request
    if request.method == "POST":
        try:
            # Get the shopping cart and the seedling item by its ID
            cart = Cart(request)
            seedling = get_object_or_404(Seedling, id=item_id)

            # Add the seedling to the cart, converting the price to a float
            cart.add(item_id=seedling.id, quantity=1, price=float(seedling.price))

            # Return a success response with a message and the item's name and price
            return JsonResponse({
                "success": True,
                "message": "Item added to cart successfully!",
                "item_name": seedling.name,
                "item_price": float(seedling.price)  # Convert price to float for JSON compatibility
            })
        except Exception as e:
            # If an error occurs, log the error and return a failure response
            print(f"Error adding item to cart: {e}")
            return JsonResponse({"success": False, "error": "Something went wrong. Please try again."}, status=500)
    else:
        # If the request method is not POST, return an error response
        return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)
# cart items
def cart(request):
    cart_items = CartItem.objects.all()
    for item in cart_items:
        item.total_price = item.seedling.price * item.quantity
    total_price = sum(item.total_price for item in cart_items)
    context = {'cart_items': cart_items, 'total': total_price if total_price > 0 else 0}
    return render(request, 'cart.html', context)


def remove_cart_item(request, item_id):
    # Your logic to remove the item from the cart
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
    request.session['cart'] = cart

    # Calculate the new total
    cart_total = sum(item['price'] * item['quantity'] for item in cart.values())

    return JsonResponse({
        'success': True,
        'cart_total': cart_total
    })


def update_cart_item(request, item_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity', 1)

            # Get the cart from session
            cart = Cart(request)

            # Check if the item is in the cart, then update it
            if item_id in cart.cart:
                cart.cart[item_id]['quantity'] = quantity
                cart.save()

                # Recalculate the item total and cart total
                item_total = cart.cart[item_id]['price'] * quantity
                cart_total = cart.get_total_price()

                return JsonResponse({
                    "success": True,
                    "item_total": item_total,
                    "cart_total": cart_total,
                })
            else:
                return JsonResponse({"success": False, "error": "Item not found in cart"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)



def checkout(request):
    cart = request.session.get("cart", {})
    # Calculate the total for each item in the cart
    for item in cart.values():
        item['total'] = item['quantity'] * item['price']  # Add a 'total' key for each item
    total = sum(item["total"] for item in cart.values())  # Total for the entire cart
    return render(request, 'checkout.html', {"cart": cart, "total": total})




def mpesaapi(request):
    client = MpesaClient()
    phone_number = '0708691113'
    amount = 1
    account_reference = 'eMobilis'
    transaction_dec = 'payment for web dev'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = client.stk_push(phone_number, amount, transaction_dec, account_reference, callback_url)
    return HttpResponse(response)