from django.shortcuts import render, redirect
from .models import Student_jzdn, Degree_jzdn
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages  # Add this import
from django.contrib.messages.views import SuccessMessageMixin  # Add this import

class StudentListView_jzdn(ListView):
    model = Student_jzdn
    template_name = 'student_register_jzdn/student_list.html'
    context_object_name = 'students'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        degree_id = self.request.GET.get('degree')
        if degree_id:
            queryset = queryset.filter(degree_id=degree_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['degrees'] = Degree_jzdn.objects.all()
        
        # Add current filter to context for pagination links
        degree_filter = self.request.GET.get('degree', '')
        if degree_filter:
            context['current_degree_filter'] = degree_filter
            
        return context

# Optional: Add SuccessMessageMixin for user feedback
class StudentCreateView_jzdn(SuccessMessageMixin, CreateView):
    model = Student_jzdn
    template_name = 'student_register_jzdn/student_form.html'
    fields = '__all__'
    success_url = reverse_lazy('student_list_jzdn')
    success_message = "Student was created successfully!"

class StudentUpdateView_jzdn(SuccessMessageMixin, UpdateView):
    model = Student_jzdn
    template_name = 'student_register_jzdn/student_form.html'
    fields = '__all__'
    success_url = reverse_lazy('student_list_jzdn')
    success_message = "Student was updated successfully!"

class StudentDeleteView_jzdn(SuccessMessageMixin, DeleteView):
    model = Student_jzdn
    template_name = 'student_register_jzdn/student_confirm_delete.html'
    success_url = reverse_lazy('student_list_jzdn')
    
    # Optional: Add success message after deletion
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Student was deleted successfully!")
        return super().delete(request, *args, **kwargs)