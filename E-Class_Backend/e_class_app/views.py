import hashlib
import json
import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.middleware import csrf
from django import forms
from django.core.mail import send_mail
from django.core import serializers
from .models import *
from django.views.decorators.cache import cache_page
from django.core.validators import RegexValidator

from datetime import timedelta
from datetime import date
from django.http import HttpResponse

if settings.DEBUG:
    BASE_URL = "http://127.0.0.1:8081"
else:
    BASE_URL = "https://e-class-frontend.herokuapp.com"


def index(request):
    return JsonResponse({'message': 'Hello, world!'})


def csrf_token(request):
    csrf_token = csrf.get_token(request)
    return response({'csrf_token': csrf_token})


def images(request, image_name):
    if request.method == 'GET':
        if image_name is None:
            return response({'message': 'Invalid image name!'}, 400)

        try:
            image = open('media/images/' + image_name, 'rb')
            return FileResponse(image)
        except Exception as e:
            print(e)
            return response({'message': 'Image not found!'}, 404)

    return response({'message': 'Invalid request method!'}, 405)


def login(request):
    if request.method == 'POST':

        class LoginForm(forms.Form):
            email = forms.EmailField()
            password = forms.CharField(widget=forms.PasswordInput)

        data = json.loads(request.body)
        form = LoginForm(data)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            password = hashed_password(password)

            user = User.objects.filter(email=email, password=password)

            if user:
                user = user[0]

                userDTO = UserDTO(user).__dict__

                return response(
                    data={
                        'message': 'Login successful!',
                        'user': userDTO,
                    },
                    headers={
                        "Authorization":
                        "Bearer " + jwt.encode(
                            userDTO, settings.SECRET_KEY, algorithm='HS256'),
                    })

            return response({'message': 'Invalid email or password!'}, 401)

        return response({'message': 'Invalid form data!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def signup(request):
    # This view aims to create a new user and save it into the database. After a successful
    # signup, it should automatically log in the user and redirects them to home
    # p.s if cant automatically log in, redirect to login
    if request.method == 'POST':
        class SignUpForm(forms.Form):
            username = forms.CharField()
            email = forms.EmailField()
            password = forms.CharField()
            phone_number = forms.CharField()
            is_teacher = forms.BooleanField()

        data = json.loads(request.body)
        form = SignUpForm(data)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            is_teacher = form.cleaned_data['is_teacher']

            if is_teacher:
                is_teacher = "teacher"
            else:
                is_teacher = "student"

            password = hashed_password(password)

            user = User.objects.filter(email=email, password=password)

            if user:
                return response({'message': 'Email already used!'}, 401)

            new_user = User(
                username=username,
                password=password,
                email=email,
                phone_number=phone_number,
                user_type=is_teacher,
            )

            new_user.save()

            user = User.objects.filter(email=email, password=password)

            if user:

                user = user[0]

                userDTO = UserDTO(user).__dict__

                return response(
                    data={
                        'message': 'Signup successful! Logging in...',
                        'user': userDTO,
                    },
                    headers={
                        "Authorization":
                            "Bearer " + jwt.encode(
                                userDTO, settings.SECRET_KEY, algorithm='HS256'),
                    })

        return response({'message': 'Invalid form data!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def forgot_password(request):
    if request.method == 'POST':

        class ForgotPasswordForm(forms.Form):
            email = forms.EmailField()

        data = json.loads(request.body)
        form = ForgotPasswordForm(data)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()

            user = User.objects.filter(email=email)

            if user:
                user = user[0]

                reset_password_token = jwt.encode({
                    'user_id': user.user_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },

                    settings.SECRET_KEY,
                    algorithm='HS256')

                # add "/" to the end of the path to prevent 404 error due to the dot in the token
                reset_password_link = f"{BASE_URL}/reset-password/{reset_password_token}/"

                send_mail(
                    subject="E-Class Password Reset",
                    message=(
                        "Hello, " + user.username + "!" +
                        " Please follow this link to reset your password: " + reset_password_link +
                        " The link will expire in 15 minutes." +
                        " Do NOT share this link with anyone." +
                        " If you did not request a password reset, please ignore this email."
                    ),
                    from_email=None,  # webmaster@localhost
                    recipient_list=[user.email],
                    fail_silently=False,
                    html_message=(
                        "Hello, " + user.username + "!" + "<br><br>" +
                        "Please follow this link to reset your password: " + "<br>" +
                        "<a href='" + reset_password_link + "'>" + reset_password_link + "<a>" + "<br><br>" +
                        "The link will expire in 15 minutes." + "<br><br>" +
                        "Do NOT share this link with anyone." + "<br><br>" +
                        "If you did not request a password reset, please ignore this email."
                    ),
                )

            return response({'message': 'Password reset link sent to ' + user.email + ' if it exists!'})

        return response({'message': 'Invalid form data!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def validate_reset_password_token(request):
    if request.method == 'POST':

        class ValidateResetPasswordTokenForm(forms.Form):
            reset_password_token = forms.CharField()

        data = json.loads(request.body)
        form = ValidateResetPasswordTokenForm(data)

        if form.is_valid():
            try:
                reset_password_token = jwt.decode(
                    data['reset_password_token'], settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.exceptions.ExpiredSignatureError:
                return response({'message': 'Token expired!'}, 400)

            user = User.objects.filter(user_id=reset_password_token['user_id'])

            if user:
                user = user[0]

                return response({'message': 'Token valid!', 'user': UserDTO(user).__dict__})

            return response({'message': 'Invalid reset password token!'}, 400)

        return response({'message': 'Invalid form data!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def reset_password(request):
    if request.method == 'POST':

        class ResetPasswordForm(forms.Form):
            password = forms.CharField(widget=forms.PasswordInput)
            confirm_password = forms.CharField(widget=forms.PasswordInput)

        data = json.loads(request.body)
        form = ResetPasswordForm(data)

        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return response({'message': 'Passwords do not match!'}, 400)

            try:
                reset_password_token = jwt.decode(
                    data['reset_password_token'], settings.SECRET_KEY, algorithms=['HS256'])

            except jwt.exceptions.ExpiredSignatureError:
                return response({'message': 'Token expired!'}, 400)

            user = User.objects.filter(user_id=reset_password_token['user_id'])

            if user:
                user = user[0]

                user.password = hashed_password(password)
                user.save()
                return response({'message': 'Password reset successful!'})

            return response({'message': 'Invalid reset password token!'}, 400)

        return response({'message': 'Invalid form data!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


# @cache_page(60 * 1)  # Cache for 10 minutes （60 means 60 second）
def courses_me(request):
    if request.method == 'GET':
        auth_token = get_auth_token_from_request(request)
        if auth_token is None:
            return response({'message': 'Invalid or expired authentication token!'}, 400)

        user = get_user_from_token(auth_token)
        if user is None:
            return response({'message': 'No user found!'}, 400)

        teachingCourses = Course.objects.filter(teacher_id=user.user_id)
        teachingCourses = [
            CourseDTO(course).__dict__ for course in teachingCourses]

        learningCourses = Course.objects.filter(course_id__in=Classroom.objects.filter(classroom_id__in=StudentClassroom.objects.filter(student_id=user.user_id)
                                                                                       .values_list('class_id', flat=True))
                                                .values_list('course_id', flat=True))
        learningCourses = [
            CourseDTO(course).__dict__ for course in learningCourses]

        return response({'message': 'Course list retrieved!',
                         'teachingCourses': teachingCourses,
                         'learningCourses': learningCourses})

    return response({'message': 'Invalid request method!'}, 405)


def course_id(request, course_id):
    if request.method == 'GET':
        auth_token = get_auth_token_from_request(request)
        if auth_token is None:
            return response({'message': 'Invalid or expired authentication token!'}, 400)

        user = get_user_from_token(auth_token)
        if user is None:
            return response({'message': 'No user found!'}, 400)

        if course_id is None:
            return response({'message': 'Invalid course_id!'}, 400)

        # course
        course = Course.objects.filter(course_id=course_id)
        if course is None:
            return response({'message': 'Course not found!'}, 404)

        if user.user_id == course[0].teacher_id.user_id:
            # TODO: return course info for teacher
            return response({'message': 'To be implemented!'}, 501)
        else:
            # TODO: return course info for student
            classroom = Classroom.objects.filter(classroom_id__in=StudentClassroom.objects.filter(student_id=user.user_id)
                                                 .values_list('class_id', flat=True),
                                                 course_id=course_id)

            if not classroom:
                return response({'message': 'Course not found!'}, 404)

            # lessons
            lessons = Lesson.objects.filter(course_id=course_id)
            lessons = [LessonDTO(lesson).__dict__ for lesson in lessons]

            # quizzes
            quizzes = Quiz.objects.filter(lesson_id__in=Lesson.objects.filter(
                course_id=course_id)
                .values_list('lesson_id', flat=True))
            QuizAttempts = QuizAttempt.objects.filter(quiz_id__in=quizzes.values_list('quiz_id', flat=True),
                                                      student_id=user.user_id)
            quizzes = [QuizDTO(quiz, QuizAttempts.filter(
                quiz_id=quiz.quiz_id).count()).__dict__ for quiz in quizzes]

            return response({'message': 'Course retrieved!',
                             'target': 'student',  # 'teacher' or 'student'
                             'course': CourseDTO(course[0]).__dict__,
                             'classroom': ClassroomDTO(classroom[0]).__dict__,
                             'lessons': lessons,
                             'quizzes': quizzes})

    return response({'message': 'Invalid request method!'}, 405)


def users_me(request):
    if request.method == 'GET':
        auth_token = get_auth_token_from_request(request)
        if auth_token is None:
            return response({'message': 'Invalid or expired authentication token!'}, 400)

        user = get_user_from_token(auth_token)
        if user is None:
            return response({'message': 'No user found!'}, 400)

        return response(
            data={
                'message': 'Login successful!',
                'user': UserDTO(user).__dict__,
            },
            headers={
                "Authorization": "Bearer " + jwt.encode(UserDTO(user).__dict__, settings.SECRET_KEY, algorithm='HS256'),
            })

    return response({'message': 'Invalid request method!'}, 405)


@cache_page(60 * 1)
def users_messages(request):
    if request.method == 'GET':
        if 'Bearer ' in request.headers["Authorization"]:
            auth_token = request.headers["Authorization"].split(' ')[1]

            try:
                userDTO = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[
                                     'HS256'], options={"require": ["user_id"]})
            except Exception as e:
                return response({'message': 'Invalid or expired token! ' + str(e)}, 400)

            user = User.objects.filter(user_id=userDTO['user_id'])

            if user:
                user = user[0]

                recentMessagesQuery = Message.objects.filter(
                    receiver_id=user.user_id)

                if 'recent' in request.GET and request.GET['recent'] == 'true':
                    # Order messages by sent_time (from newest to oldest) and take the first two message
                    recentMessagesQuery = recentMessagesQuery.order_by(
                        '-sent_time')[:3]

                recentMessages = [MessageDTO(
                    message).__dict__ for message in recentMessagesQuery]

                return response({'message': 'recentMessages retrieved!',
                                 'recentMessages': recentMessages})

            return response({'message': 'No user found!'}, 400)

        return response({'message': 'Invalid or expired token!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


@cache_page(60 * 1)
def users_payments(request):
    if request.method == 'GET':
        if 'Bearer ' in request.headers["Authorization"]:
            auth_token = request.headers["Authorization"].split(' ')[1]

            try:
                userDTO = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[
                                     'HS256'], options={"require": ["user_id"]})
            except Exception as e:
                return response({'message': 'Invalid or expired token! ' + str(e)}, 400)

            user = User.objects.filter(user_id=userDTO['user_id'])

            if user:
                user = user[0]

                recentMessagesQuery = Payment.objects.filter(
                    student_id_id=user.user_id)

                if 'recent' in request.GET and request.GET['recent'] == 'true':
                    # Order messages by sent_time (from newest to oldest) and take the first two message
                    recentMessagesQuery = recentMessagesQuery.order_by(
                        '-create_time')

                recentMessages = [PaymentDTO(
                    message).__dict__ for message in recentMessagesQuery]

                return response({'message': 'recentMessages retrieved!',
                                 'recentMessages': recentMessages})

            return response({'message': 'No user found!'}, 400)

        return response({'message': 'Invalid or expired token!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def apply_course(request):
    # for getting the course's information to display when applying
    if request.method == 'GET':
        current_course = Course.objects.get(
            course_id=request.GET.get('course_id', None))
        teacher_id = current_course.teacher_id_id

        teacher = User.objects.filter(user_id=teacher_id)
        teacher = teacher[0]
        teacher = UserDTO(teacher)

        data = {
            "name": teacher.username,
            "fee": current_course.fee
        }

        return response(data)
    # NEED TO IMPLEMENT

    elif request.method == 'POST':

        class applyCourseForm(forms.Form):
            extra_info = forms.CharField(label="extra_info", max_length=200)
            online = forms.BooleanField(label="online")
            address = forms.CharField(label="address")
            phone_number = forms.CharField(error_messages=" invalid; Enter a phone number", validators=[
                                           RegexValidator(r"^[0-9]+$", "Enter a valid phone number.")])

        data = json.loads(request.body)
        form = applyCourseForm(data)

        # if form.is_valid():


@cache_page(60 * 3)
def course_search(request):
    if request.method == 'GET':
        course_name = request.GET.get('search_coursename', None)
        print("course name: " + course_name)
        if course_name:
            courses = Course.objects.filter(
                name__icontains=course_name, status='active')
            if courses:
                searchCourseResults = [
                    CourseDTO(course).__dict__ for course in courses]

                return response({'message': 'search courses retrieved!',
                                'searchResult': searchCourseResults})

            return response({'message': 'No courses found!',
                             'searchResult': None})

        return response({'message': 'Invalid search input!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


@cache_page(60 * 3)
def dashboard_courses(request):
    if request.method == 'GET':
        if 'Bearer ' in request.headers["Authorization"]:
            auth_token = request.headers["Authorization"].split(' ')[1]

            try:
                userDTO = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[
                                     'HS256'], options={"require": ["user_id"]})
            except Exception as e:
                return response({'message': 'Invalid or expired token! ' + str(e)}, 400)

            user = User.objects.filter(user_id=userDTO['user_id'])

            if user:
                user = user[0]
                if user.user_type == 'student':
                    classrooms_for_student = Classroom.objects.filter(
                        studentclassroom__student_id=user.user_id)

                    filtered_classrooms = filter_classrooms(
                        classrooms_for_student)

                    course_ids = [
                        classroom.course_id_id for classroom in filtered_classrooms]
                    courses = Course.objects.filter(course_id__in=course_ids)

                    print(courses)
                    if courses:
                        searchCourseResults = [
                            CourseDTO(course).__dict__ for course in courses]

                        return response({'message': 'student dashboard courses retrieved!',
                                        'courseResult': searchCourseResults})

                    return response({'message': 'student No courses found!',
                                    'courseResult': None})

                if user.user_type == 'teacher':
                    courses = Course.objects.filter(
                        teacher_id=user.user_id, status='active')
                    if courses:
                        searchCourseResults = [
                            CourseDTO(course).__dict__ for course in courses]

                        return response({'message': 'teacher dashboard courses retrieved!',
                                        'courseResult': searchCourseResults})

                    return response({'message': 'teacher No courses found!',
                                    'courseResult': None})

            return response({'message': 'No user found!'}, 400)

        return response({'message': 'Invalid or expired token!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


@cache_page(60 * 3)  # Cache for 10 minutes （60 means 60 second）
def view_course(request):

    if request.method == 'GET':
        current_course = Course.objects.get(
            course_id=request.GET.get('course_id', None))
        # print(current_course.course_id)
        # print(current_course.description)

        lessons = Lesson.objects.filter(course_id=current_course.course_id)
        reviews = CourseReview.objects.filter(
            course_id=current_course.course_id)
        classrooms = Classroom.objects.filter(
            course_id=current_course.course_id)
        teacher = User.objects.get(user_id=current_course.teacher_id_id)

        lessons = [LessonDTO(lesson).__dict__ for lesson in lessons]
        reviews = [CourseReviewDTO(review).__dict__ for review in reviews]
        classrooms = [ClassroomDTO(
            classroom).__dict__ for classroom in classrooms]

        course = CourseDTO(current_course).__dict__
        teacher = UserDTO(teacher).__dict__

        # print(lessons)
        print(classrooms)
        data = {
            "lessons": lessons,
            "reviews": reviews,
            "course": course,
            "teacher": teacher,
            "classrooms": classrooms
        }
        # print(current_course)

        return response(data)


@cache_page(60 * 3)
def view_classroom(request):

    if request.method == 'GET':
        current_classroom = Classroom.objects.get(
            classroom_id=request.GET.get('classroom_id', None))
        # print(current_classroom.classroom_id)

        classrooms = Classroom.objects.get(
            classroom_id=current_classroom.classroom_id)
        people_in = StudentClassroom.objects.filter(
            class_id_id=current_classroom.classroom_id)

        classrooms = ClassroomDTO(classrooms).__dict__
        people_in = [StudentClassroomDTO(
            people).__dict__ for people in people_in]
        print(people_in)
        # print(classrooms)
        data = {

            "classroom": classrooms,
            "people_in": len(people_in)
        }

        return response(data)


def dashboard_quiz(request):
    if request.method == 'GET':
        if 'Bearer ' in request.headers["Authorization"]:
            auth_token = request.headers["Authorization"].split(' ')[1]

            try:
                userDTO = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[
                                     'HS256'], options={"require": ["user_id"]})
            except Exception as e:
                return response({'message': 'Invalid or expired token! ' + str(e)}, 400)

            user = User.objects.filter(user_id=userDTO['user_id'])

            if user:
                user = user[0]
                if user.user_type == 'student':
                    classrooms_for_student = StudentClassroom.objects.filter(
                        student_id_id=user.user_id)
                    classrooms = Classroom.objects.filter(
                        classroom_id__in=[classroom.class_id_id for classroom in classrooms_for_student])

                    filtered_classrooms = filter_classrooms(classrooms)

                    # classrooms =
                    quizes = Quiz.objects.filter(lesson_id_id__in=[
                                                 classroom.current_lesson_id_id for classroom in filtered_classrooms])

                    print(quizes)
                    if quizes:
                        quizResults = [
                            QuizDTO_Dashboard(course).__dict__ for course in quizes]

                        return response({'message': 'student dashboard quizes retrieved!',
                                        'quizResult': quizResults})

                    return response({'message': 'student No quizes found!',
                                    'quizResult': None})

                if user.user_type == 'teacher':
                    courses = Course.objects.filter(teacher_id=user.user_id)
                    classrooms = Classroom.objects.filter(
                        course_id_id__in=[course.course_id for course in courses])

                    filtered_classrooms = filter_classrooms(classrooms)

                    current_lesson_id = [
                        classroom.current_lesson_id_id for classroom in filtered_classrooms]
                    quizes = Quiz.objects.filter(
                        lesson_id_id__in=current_lesson_id)
                    print(quizes)
                    if quizes:
                        quizResults = [
                            QuizDTO_Dashboard(course).__dict__ for course in quizes]

                        return response({'message': 'teacher dashboard quizes retrieved!',
                                        'quizResult': quizResults})

                    return response({'message': 'teacher No quizes found!',
                                    'courseResult': None})

                return response({'message': 'recentMessages retrieved!',
                                 'recentMessages': 'none'})

            return response({'message': 'No user found!'}, 400)

        return response({'message': 'Invalid or expired token!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def payment(request):
    if request.method == 'GET':
        print('course_id')
        current_course = Course.objects.get(
            course_id=request.GET.get('course_id', None))
        print(current_course.course_id)
        print(current_course.teacher_id)

        current_tutor = User.objects.get(user_id=current_course.teacher_id_id)
        tutorname = current_tutor.username

        data = {
            "coursename": current_course.name,
            "tutorname": tutorname,
            "classprice": current_course.fee
        }

    return response(data)


def change_information(request):
    if request.method == 'POST':
        class newUserInformation(forms.Form):
            new_username = forms.CharField()
            new_email = forms.CharField()
            old_email = forms.CharField()
            new_phone_number = forms.CharField()
            given_password = forms.CharField(widget=forms.PasswordInput)

        data = json.loads(request.body)
        form = newUserInformation(data)

        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            new_email = form.cleaned_data['new_email']
            old_email = form.cleaned_data['old_email']
            new_phone_number = form.cleaned_data['new_phone_number']
            given_password = form.cleaned_data['given_password']

            given_password = hashed_password(given_password)

            user = User.objects.filter(
                email=old_email, password=given_password)

            if user:
                user = user[0]

                user.username = new_username
                user.email = new_email
                user.phone_number = new_phone_number

                user.save()

                userDTO = UserDTO(user).__dict__

                return response(
                    data={
                        'message': 'Information Successfully Changed!',
                        'user': userDTO,
                    }
                )

            return response({'message': 'Invalid Password!'}, 401)

        return response({'message': 'Invalid form data!'}, 400)

    return response({'message': 'Invalid request method!'}, 405)


def message(request):

    if request.method == 'GET':
        current_user = User.objects.get(
            user_id=request.GET.get('user_id', None))

        received_messages = Message.objects.filter(
            receiver_id=current_user.user_id)
        received_messages = [MessageDTO(
            message).__dict__ for message in received_messages]

        messages_sent = Message.objects.filter(sender_id=current_user.user_id)
        messages_sent = [MessageDTO(
            message).__dict__ for message in messages_sent]

        data = {
            "received_messages": received_messages,
            "messages_sent": messages_sent
        }
        # print(current_course)

        return response(data)

# Helper function to return a JSON response


def response(data, status_code=200, headers=None):
    response = JsonResponse(headers=headers, data=data)
    response.status_code = status_code
    return response


def hashed_password(password):
    sha256 = hashlib.sha256()

    sha256.update(password.encode('utf-8'))

    hashed_password = sha256.hexdigest()
    return hashed_password


def get_auth_token_from_request(request):
    if 'Bearer ' in request.headers["Authorization"]:
        auth_token = request.headers["Authorization"].split(' ')[1]
        return auth_token

    return None


def get_user_from_token(auth_token):
    try:
        userDTO = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=[
                             'HS256'], options={"require": ["user_id"]})
    except Exception as e:
        print(e)
        return None

    user = User.objects.filter(user_id=userDTO['user_id'])

    if user:
        user = user[0]
        return user

    return None


def filter_classrooms(classrooms, reference_date=None):
    """
    Filters classrooms based on recurrence and checks if the end date is later than today's date.

    :param classrooms: List of classrooms to be filtered.
    :param reference_date: Optional. A specific date to compare against. Defaults to today's date.
    :return: A list of filtered classrooms.
    """

    if reference_date is None:
        reference_date = date.today()

    filtered_classrooms = []

    for classroom in classrooms:
        if classroom.recurrence == 'DAILY':
            delta = timedelta(days=1)
        elif classroom.recurrence == 'WEEKLY':
            delta = timedelta(days=7)
        elif classroom.recurrence == 'MONTHLY':
            delta = timedelta(days=30)
        else:
            delta = timedelta(days=1)

        end_date = classroom.start_time + (delta * classroom.repeat_every)

        if end_date.date() > reference_date:
            filtered_classrooms.append(classroom)

    return filtered_classrooms

# Helper classes to convert models to JSON


class UserDTO:

    def __init__(self, user):
        self.user_id = user.user_id
        self.username = user.username
        self.email = user.email
        self.phone_number = user.phone_number
        self.user_type = user.user_type
        self.profile_image = user.profile_image.url if user.profile_image else None


class CourseDTO:

    def __init__(self, course):
        self.course_id = course.course_id
        self.teacher = UserDTO(
            course.teacher_id).__dict__ if course.teacher_id else None
        self.name = course.name
        self.description = course.description
        self.main_image_url = course.main_image_url.image_url if course.main_image_url else None
        self.fee = course.fee
        self.status = course.status
        if course.main_image_url:
            self.main_image_url = course.main_image_url.image_url


class ClassroomDTO:
    def __init__(self, classroom):
        self.classroom_id = classroom.classroom_id
        self.course_id = classroom.course_id.course_id
        self.current_lesson_id = classroom.current_lesson_id.lesson_id
        self.no_student = classroom.no_student
        self.name = classroom.name
        self.start_time = classroom.start_time
        self.recurrence = classroom.recurrence
        self.repeat_every = classroom.repeat_every
        self.location = classroom.location


class MessageDTO:

    def __init__(self, message):
        self.message_id = message.message_id
        self.content = message.content
        self.sent_time = message.sent_time

        # Including sender and receiver details
        self.sender_id = message.sender_id.user_id
        self.sender_username = message.sender_id.username
        self.sender_user_type = message.sender_id.user_type

        self.receiver_id = message.receiver_id.user_id
        self.receiver_username = message.receiver_id.username
        self.receiver_user_type = message.receiver_id.user_type


class QuizDTO:
    def __init__(self, quiz):
        self.quiz_id = quiz.quiz_id
        self.lesson_id = quiz.lesson_id_id
        self.name = quiz.name
        self.description = quiz.description
        self.no_max_attempt = quiz.no_max_attempt
        self.time_limit_minute = quiz.time_limit_minute


class QuizDTO_Dashboard:
    def __init__(self, quiz):
        self.quiz_id = quiz.quiz_id

        # Get the related Lesson instance
        lesson = quiz.lesson_id
        self.lesson_id = lesson.lesson_id
        self.lesson_name = lesson.name

        # Get the related Course instance from the lesson
        course = lesson.course_id
        self.course_id = course.course_id
        self.course_name = course.name

        self.name = quiz.name
        self.description = quiz.description
        self.no_max_attempt = quiz.no_max_attempt
        self.time_limit_minute = quiz.time_limit_minute


class LessonDTO:
    def __init__(self, lesson):
        self.lesson_id = lesson.lesson_id
        self.course_id = lesson.course_id.course_id
        self.name = lesson.name
        self.description = lesson.description
        self.duration_minute = lesson.duration_minute
        self.order_number = lesson.order_number


class CourseReviewDTO:
    def __init__(self, course_review):
        self.review_id = course_review.review_id
        self.course_id = course_review.course_id.course_id
        self.student_id = course_review.student_id.user_id
        self.student_name = course_review.student_id.username
        self.rating = course_review.rating
        self.comment = course_review.comment
        self.date = course_review.date


class ClassroomDTO:
    def __init__(self, classroom):
        self.classroom_id = classroom.classroom_id
        self.course_id = classroom.course_id.course_id
        self.current_lesson_id = classroom.current_lesson_id.lesson_id if classroom.current_lesson_id else None
        self.no_student = classroom.no_student
        self.name = classroom.name
        self.start_time = classroom.start_time
        self.recurrence = classroom.recurrence
        self.repeat_every = classroom.repeat_every
        self.location = classroom.location


class StudentClassroomDTO:
    def __init__(self, student_classroom):
        self.classroom_id = student_classroom.class_id.classroom_id
        self.student_id = student_classroom.student_id.user_id


class PaymentDTO:
    def __init__(self, payment):
        self.payment_id = payment.payment_id
        self.amount = payment.amount
        self.create_time = payment.create_time
        self.status = payment.status
        self.method = payment.method
        self.course_id = payment.course_id.course_id
        self.course_name = payment.course_id.name
        self.student_id_id = payment.student_id.user_id


class QuizDTO:
    def __init__(self, quiz, no_attempt=None):
        self.quiz_id = quiz.quiz_id
        self.lesson_id = quiz.lesson_id.lesson_id
        self.name = quiz.name
        self.description = quiz.description
        self.no_max_attempt = quiz.no_max_attempt
        self.time_limit_minute = quiz.time_limit_minute
        self.no_attempt = no_attempt
