from django import forms
from .models import Student

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('student_number','first_name','middle_name','last_name','email','degree')
        labels = {
            'student_number':'Student.No',
            'first_name':'First Name',
            'middle_name':'Middle Name',
            'last_name':'Last Name',
            'email':'Email',
            'degree':'Degree'
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm,self).__init__(*args, **kwargs)
        self.fields['degree'].empty_label = "Select"
