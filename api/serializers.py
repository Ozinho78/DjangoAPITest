from rest_framework import serializers
from students.models import Student
from employees.models import Employee


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"  # in diesem Serializer werden alle Felder des Modells Student abgefragt


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

