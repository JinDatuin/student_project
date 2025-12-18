from django.urls import path
from .views import StudentListView_jzdn, StudentCreateView_jzdn, StudentUpdateView_jzdn, StudentDeleteView_jzdn

urlpatterns = [
    path('', StudentListView_jzdn.as_view(), name='student_list_jzdn'),
    path('new/', StudentCreateView_jzdn.as_view(), name='student_new_jzdn'),
    path('edit/<int:pk>/', StudentUpdateView_jzdn.as_view(), name='student_edit_jzdn'),
    path('delete/<int:pk>/', StudentDeleteView_jzdn.as_view(), name='student_delete_jzdn'),
]
