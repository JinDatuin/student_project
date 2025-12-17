from django import forms
from .models import Student, Degree
from django.core.validators import EmailValidator, RegexValidator
import re

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ('student_number', 'first_name', 'middle_name', 'last_name', 'email', 'degree')
        labels = {
            'student_number': 'Student Number',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'degree': 'Degree Program'
        }
        
        # Custom help texts
        help_texts = {
            'student_number': 'Enter unique student identification number',
            'email': 'Enter a valid email address (will be used for communication)',
            'degree': 'Select the degree program the student is enrolled in'
        }
        
        # Custom error messages
        error_messages = {
            'student_number': {
                'required': 'Student number is required',
                'unique': 'This student number already exists'
            },
            'email': {
                'required': 'Email address is required',
                'invalid': 'Enter a valid email address'
            }
        }
        
        # Custom widgets for better styling
        widgets = {
            'student_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., STU-2024-001',
                'autocomplete': 'off',
                'data-toggle': 'tooltip',
                'title': 'Unique identifier for the student'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
                'autocomplete': 'given-name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter middle name (optional)',
                'autocomplete': 'additional-name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
                'autocomplete': 'family-name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@example.com',
                'autocomplete': 'email'
            }),
            'degree': forms.Select(attrs={
                'class': 'form-select',
                'id': 'degree-select'
            })
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        
        # Populate degree choices from the database
        self.fields['degree'].queryset = Degree.objects.all()
        self.fields['degree'].empty_label = "Select Degree Program"
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.widgets:
                if 'class' not in field.widget.attrs:
                    if isinstance(field.widget, forms.Select):
                        field.widget.attrs['class'] = 'form-select'
                    else:
                        field.widget.attrs['class'] = 'form-control'
            
            # Add data attributes for JavaScript
            field.widget.attrs['data-field'] = field_name
            
            # Add ARIA labels for accessibility
            if field.label:
                field.widget.attrs['aria-label'] = field.label

        # Set required attribute explicitly for better UX
        self.fields['student_number'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['degree'].required = True
        self.fields['middle_name'].required = False

    # Custom validation methods
    def clean_student_number(self):
        student_number = self.cleaned_data.get('student_number')
        
        # Remove any spaces and convert to uppercase
        student_number = student_number.strip().upper()
        
        # Check uniqueness (handled by model, but can add custom message)
        if Student.objects.filter(student_number=student_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                f"A student with number {student_number} already exists.",
                code='duplicate_student_number'
            )
        
        return student_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.strip().lower()
        
        # Check uniqueness
        if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                f"Email {email} is already registered to another student.",
                code='duplicate_email'
            )
        
        # Additional email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError(
                "Please enter a valid email address.",
                code='invalid_email_format'
            )
        
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Capitalize first letter of each word
            first_name = ' '.join(word.capitalize() for word in first_name.split())
            
            # Remove extra spaces
            first_name = ' '.join(first_name.split())
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            # Capitalize first letter of each word
            last_name = ' '.join(word.capitalize() for word in last_name.split())
            
            # Remove extra spaces
            last_name = ' '.join(last_name.split())
        return last_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data.get('middle_name')
        if middle_name:
            # Capitalize first letter of each word
            middle_name = ' '.join(word.capitalize() for word in middle_name.split())
            
            # Remove extra spaces
            middle_name = ' '.join(middle_name.split())
        return middle_name

    def clean(self):
        cleaned_data = super().clean()
        
        # Cross-field validation example
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name and last_name and first_name.lower() == last_name.lower():
            raise forms.ValidationError(
                "First name and last name should not be identical.",
                code='identical_names'
            )
        
        return cleaned_data
