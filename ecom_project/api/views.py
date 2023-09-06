from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from  django.urls import reverse
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import csv
from .models import Product
from .models import Review
from django.core.paginator import Paginator
from django.db.models import Avg


# Other imports...

# Register userprofile
def register(request):
    if request.method == 'POST':
        print("hello", request.method)
        
        # Check if all required fields are present in the POST data
        if all(request.POST.get(field) for field in ["first_name", "last_name", "email", "phone", "password"]):
            try:
                # Check if the email already exists in the database
                UserProfile.objects.get(email=request.POST.get("email"))
                return HttpResponse("Sorry, email already exists")
            except UserProfile.DoesNotExist:
                # Create a new UserProfile
                user = UserProfile(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    email=request.POST.get("email"),
                    phone=request.POST.get("phone"),
                    password=request.POST.get("password")


                )
                user.save()
                return HttpResponse("User registered successfully")
        else:
            return HttpResponse("Please fill out all fields")
    else:
        return render(request, 'api/registration.html')



def login(request):
    if request.method == 'GET':
        return render(request, 'api/login.html')
    else:
        print(request.POST)
        user = UserProfile.objects.filter(email=request.POST.get("email"), password=request.POST.get("password"))
        if len(user) > 0:
            # Use reverse without the namespace to construct the URL
            return HttpResponseRedirect(reverse("api:product"))

        else:
            return HttpResponseRedirect(reverse("api:register"))

    


def product(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return HttpResponse('File is not a CSV', content_type='text/plain')

        csv_data = csv.reader(csv_file)
        for row in csv_data:
            product = Product(
                product_name=row[0],
                barcode=row[1],
                brand=row[2],
                description=row[3],
                price=row[4],
            )
            product.save()

        return HttpResponse('CSV file uploaded and products created successfully', content_type='text/plain')

    return render(request, "api/product.html")


def create_review(request):
    if request.method == 'POST':
        product_id = request.POST.get("product_id")
        rating = request.POST.get("rating")
        review_text = request.POST.get("review_text")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return HttpResponse("Product does not exist")

        user = request.user  

        # Create a new review
        review = Review(
            product=product,
            user=user,
            rating=rating,
            review_text=review_text,
        )
        review.save()

        return HttpResponse('Review created successfully')

    return render(request, "api/create_review.html")



def product_list(request):
    products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')

    # Paginate the product list
    paginator = Paginator(products, 10)  # Show 10 products per page

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "api/product_list.html", {'page': page})

