from django.shortcuts import render

def index(request):
  text="Home Page"
  return render(request,'base/home.html')

def about(request):
  return render (request,'base/about.html')


