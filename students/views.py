from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def students(request):
    students = [
        {'id': 1, 'name': 'John Doe', 'age': 25},
    ]
    # return HttpResponse('<h2>Hello World!</h2>')
    return HttpResponse(students)



