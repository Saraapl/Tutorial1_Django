from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

from django.views.generic import TemplateView

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Sara",
        })
        return context

from django.views import View
from django.shortcuts import render

class Product:
    products = []

    def __init__(self, name, price):
        self.id = str(len(Product.products) + 1)
        self.name = name
        self.price = price

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
            return render(request, self.template_name, {
                "title": "Product index",
                "products": Product.products,
                "total": len(Product.products), 
            })
    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products,
        }
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        product = Product.products[int(id)-1]
        viewData = {
            "title": f"{product['name']} - Online Store",
            "subtitle": f"{product['name']} - Product information",
            "product": product,
        }
        return render(request, self.template_name, viewData)


from django import forms
from django.shortcuts import redirect

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
            price = self.cleaned_data['price']
            if price < 0:
                raise forms.ValidationError("El precio no puede ser negativo.")
            return price
class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {
            "title": "Create product",
            "form": form,
        })

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
      
            Product.products.append(Product(name=name, price=price))

            return redirect('index') 
        else:
            return render(request, self.template_name, {
                "title": "Create product",
                "form": form,
            })
