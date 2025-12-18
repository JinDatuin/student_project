from django.db import models

class Degree_jzdn(models.Model):
	degree_title = models.CharField(max_length=50)
	def __str__(self):
		return self.degree_title

class Student_jzdn(models.Model):
	student_id = models.CharField(max_length=50)
	fname = models.CharField(max_length=50)
	mname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	degree = models.ForeignKey(Degree_jzdn, on_delete=models.CASCADE)
