from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    profile_image = models.ImageField(upload_to='images/', blank=True)
    certificate = models.TextField(max_length=1024, blank=True, null=True)


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_time = models.DateTimeField()


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    fee = models.FloatField()
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    main_image_url = models.ForeignKey('CourseImage', on_delete=models.SET_NULL, null=True)


class CourseReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    student_id = models.ForeignKey('User', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    date = models.DateTimeField()


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    student_id = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.FloatField()
    create_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    METHOD_CHOICES = [
        ('CreditCard', 'Credit Card'),
        ('DebitCard', 'Debit Card'),
        ('PayPal', 'PayPal'),
    ]
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='CreditCard')


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    current_lesson_id = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True)
    no_student = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    RECURRENCE_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    ]
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES)
    repeat_every = models.PositiveSmallIntegerField()
    location = models.TextField()


class Lesson(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_minute = models.IntegerField()
    order_number = models.PositiveSmallIntegerField()


class StudentClassroom(models.Model):
    class_id = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    student_id = models.ForeignKey('User', on_delete=models.CASCADE)

    # This means that a student cannot join the same classroom more than once.
    class Meta:
        unique_together = [['class_id', 'student_id']]


class CourseCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)


class CourseImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    image_url = models.TextField()


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    link = models.TextField()


class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    lesson_id = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    no_max_attempt = models.IntegerField()
    time_limit_minute = models.IntegerField()


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    content = models.TextField()
    explanation = models.TextField()


class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField()


class QuizAttempt(models.Model):
    quiz_attempt_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('User', on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    classroom_id = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    teacher_comment = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    submit_time = models.DateTimeField()


class QuizAttemptAnswer(models.Model):
    quiz_attempt_id = models.ForeignKey('QuizAttempt', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    chosen_option_id = models.ForeignKey('Option', on_delete=models.CASCADE)