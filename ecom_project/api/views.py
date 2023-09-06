from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from  django.urls import reverse
from .models import UserProfile

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


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
    


# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
       
#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             login(request, user)
#             return HttpResponse("Login successful")
#         else:
#             return HttpResponse("Invalid username or password")
#     else:
#         return render(request, 'api/login.html')

from django.urls import reverse

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

        # Assuming the CSV file has headers: product_name, barcode, brand, description, price
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




