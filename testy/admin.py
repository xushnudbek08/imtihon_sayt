from django.contrib import admin
from .models import Category, Question, AnswerOption, UserTestSession, UserAnswer, news, TestCategory
# Register your models he
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(UserTestSession)
admin.site.register(UserAnswer)
admin.site.register(news)
admin.site.register(TestCategory)
