from django.shortcuts import render
from .models import Product

# Create your views here.
def product_list(request):
    # 1. Fetch data from DB
    products = Product.objects.filter(is_active = True)

    # 2. Package data into a "context" dictionary
    context = {
        'products': products
    }

    # 3. Render HTML with data
    return render(request, 'products/product_list.html', context)