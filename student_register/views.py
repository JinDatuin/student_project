from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student
from django.core.paginator import Paginator

# Create your views here.


def student_list(request):
    student_list = Student.objects.all()
    paginator = Paginator(student_list, 10)  # Show 5 students per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "student_register/student_list.html", {'page_obj': page_obj})


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
        return redirect('/list/')


def student_delete(request,id):
    student = Student.objects.get(pk=id)
    student.delete()
    return redirect('/list/')
