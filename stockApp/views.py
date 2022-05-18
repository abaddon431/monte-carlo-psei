from django.shortcuts import render


# Create your views here.

# this is for the home views
def home(request):
    return render(request, 'stockApp/home.html', {})