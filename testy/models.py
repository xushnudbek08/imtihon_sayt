from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

class UserTestSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField()  # foydalanuvchi tanlagan vaqt
    is_finished = models.BooleanField(default=False)

class UserAnswer(models.Model):
    session = models.ForeignKey(UserTestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)





class news(models.Model):
   title = models.CharField(max_length=200)
   link = models.URLField(unique=True)
   published = models.DateTimeField()
   summary = models.TextField()

   def __str__(self):
       return self.title
   
class TestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TestQuestion(models.Model):
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE)
    question = models.TextField()
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    correct = models.CharField(max_length=1)

    def __str__(self):
        return self.question[:50]

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject