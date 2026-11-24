from django.db import models

# Create your models here.

role_type=[('Admin','Admin'),('Teacher','Teacher'),('Student','Student')]
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    role=models.CharField(max_length=100,choices=role_type)

class Quiz(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    duration=models.IntegerField(default=30)
    teacher=models.ForeignKey(User,on_delete=models.CASCADE)

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question_text=models.CharField(max_length=200)
    option_a=models.CharField(max_length=100)
    option_b=models.CharField(max_length=100)
    option_c=models.CharField(max_length=100)
    option_d=models.CharField(max_length=100)
    correct_answer=models.CharField(max_length=100)

class Result(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score=models.IntegerField()
    total_questions=models.IntegerField()

