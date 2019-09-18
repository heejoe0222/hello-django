from django.http import HttpResponse

def index(response):
    return HttpResponse("Hello, world. You're at the polls index.")
