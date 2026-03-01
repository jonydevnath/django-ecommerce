from django.db.models import Q, Avg, Sum, Min, Max
from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductForm


# Create your views here.
def product_list(request):
    # 1. Fetch data from DB
    products = Product.objects.active()

    # 2. Package data into a "context" dictionary
    context = {
        'products': products
    }

    # 3. Render HTML with data
    return render(request, 'products/product_list.html', context)

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).select_related('category').prefetch_related('tags').distinct() # optimize queries and avoids duplicates
    else:
        products = Product.objects.none()
    
    return render(request, 'products/search.html', {
        'products': products, 'query': query
    })

def category_analytics(request):
    categories = Category.objects.with_product_count().annotate(
        avg_price=Avg('products__price'),
        total_stock=Sum('products__stock'),
        min_price=Min('products__price'),
        max_price=Max('products__price')
    ).order_by('-product_count')
    
    return render(request, 'products/analytics.html', {'categories': categories})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

def low_stock_alert(request):
    products = Product.objects.low_stock().select_related('category').order_by('stock')
    return render(request, 'products/low_stock.html', {'products': products})
