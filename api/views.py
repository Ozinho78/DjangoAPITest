# from django.shortcuts import render
# from django.http import JsonResponse
from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from rest_framework import mixins, generics


# Create your views here.
@api_view(['GET', 'POST'])  # GET-Request wird für diesen View erlaubt und Interface zur Abfrage wird bereitgestellt
def studentsView(request):
    # Manuelles Serializen
    # students = Student.objects.all()    # fragt alle Studenten aus der Datenbank ab
    # print(students) # funktioniert nicht, da nicht das Dictionary geschickt wird, sondern das Query Set
    # students_list = list(students.values()) # wandelt das Query Set in eine List um = manuelles Serializen
    # students = {
    #     'id':1,
    #     'name':'Rathan',
    #     'class': 'Computer Science'
    # }
    # return JsonResponse(students)
    # return JsonResponse(students, safe=False)   # geht nicht, da "Object of type QuerySet is not JSON serializable"
    # return JsonResponse(students_list, safe=False)  # safe, weil man kein Dictionary übergibt, sondern eine List

    # Serialisierung mit Serializer
    if request.method == 'GET':
        # Get all the data from the Student table
        students = Student.objects.all()    # fragt alle Studenten aus der Datenbank ab
        serializer = StudentSerializer(students, many=True) # es gibt mehrere Studenten, also many=True, der StudentSerializer wird benutzt
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# class Employees(APIView):
#     def get(self, request):     # self, weil es eine Member-Function der Class Employees ist
#         employees = Employee.objects.all()  # alle Mitarbeiter aus der Datenbank werden abgefragt
#         serializer = EmployeeSerializer(employees, many=True)   # der EmployeeSerializer wird benutzt und es gibt mehrere Mitarbeiter
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class EmployeeDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             # return Response(status=status.HTTP_404_NOT_FOUND)
#             raise Http404

#     def get(self, request, pk):
#         employee = self.get_object(pk)  # self = die Klasse selbst betreffend
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         employee = self.get_object(pk)  # richtigen Mitarbeiter aus der Datenbank auslesen
#         serializer = EmployeeSerializer(employee, data=request.data)    # aktueller Employee und Data an den Serializer übergeben
#         if serializer.is_valid():   # prüfen, ob die Daten korrekt sind
#             serializer.save()   # Daten in die Datenbank schreiben
#             return Response(serializer.data, status=status.HTTP_200_OK) # Daten zurückgeben
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Fehler zurückgeben
    
#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# Views mit Mixins
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    


class EmployeeDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
