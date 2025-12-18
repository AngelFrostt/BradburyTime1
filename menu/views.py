from django.shortcuts import render

def menu_page(request):
    return render(request, 'menu/menu.html')  

# Create your views here.
