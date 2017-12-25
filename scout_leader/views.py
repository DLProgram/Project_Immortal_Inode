from django.shortcuts import render

# Create your views here.


def index(request):
    context = {"title": "Home"}
    return render(request, 'scout_leader/index.html', context)
