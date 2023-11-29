from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Course)
admin.site.register(CourseReview)
admin.site.register(Payment)
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(StudentClassroom)
admin.site.register(CourseCategory)
admin.site.register(CourseImage)
admin.site.register(Resource)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizAttempt)
admin.site.register(QuizAttemptAnswer)