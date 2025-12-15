from django.db import models

class Degree(models.Model):
    degree_title = models.CharField(max_length=50)

    def __str__(self):
        return self.degree_title

class Student(models.Model):
    student_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)


