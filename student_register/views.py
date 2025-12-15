from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student, Degree
from django.http import HttpResponse

def student_list(request):
    context = {'student_list': Student.objects.all()}
    return render(request, "student_register/student_list.html", context)

def student_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = StudentForm()
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(instance=student)
        return render(request, "student_register/student_form.html", {'form': form})
    else:
        if id == 0:
            form = StudentForm(request.POST)
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(request.POST,instance= student)
        if form.is_valid():
            form.save()
        return redirect('/student/list')

def student_delete(request,id):
    student = Student.objects.get(pk=id)
    student.delete()
    return redirect('/student/list')

def setup_degrees(request):
    degrees = ["Computer Science", "Information Technology", "Software Engineering", "Computer Engineering"]
    for degree_name in degrees:
        Degree.objects.get_or_create(degree_title=degree_name)
    return HttpResponse("Default degrees have been added to the database. You can now go back to the student form.")
