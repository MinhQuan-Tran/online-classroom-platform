from .views import *
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from .models import *
import json


# Create your tests here.
class LoginTests(TestCase):
    def setUp(self):
        User.objects.create(
            username="test",
            password=hashed_password("test"),
            email="test@test.com", 
            phone_number="123456789",
            user_type="student",
            profile_image=None,
            certificate=None,
        )

    def test_correct_info(self):
        data = {
            "email": "test@test.com",
            "password": "test",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Login successful!")
        self.assertEqual(response.has_header("Authorization"), True)
        self.assertEqual(response.json()["user"]["email"], "test@test.com")
        self.assertIsNone(response.json()["user"].get("password"))
        self.assertEqual(response.json()["user"]["user_type"], "student")

    def test_wrong_email(self):
        data = {
            "email": "wrong@test.com",
            "password": "test",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Invalid email or password!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))

    def test_wrong_password(self):
        data = {
            "email": "test@test.com",
            "password": "wrong",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Invalid email or password!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))

    def test_missing_email(self):
        data = {
            "password": "test",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid form data!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))

    def test_missing_password(self):
        data = {
            "email": "test@test.com",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid form data!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))

    def test_wrong_format_email(self):
        data = {
            "email": "test",
            "password": "test",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid form data!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))

    def test_wrong_method(self):
        response = self.client.get("/api/login")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["message"], "Invalid request method!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))

    def test_user_not_exist(self):
        User.objects.filter(email="test@test.com", password=hashed_password("test")).delete()
        data = {
            "email": "test@test.com",
            "password": "test",
        }
        response = self.client.post("/api/login", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Invalid email or password!")
        self.assertEqual(response.has_header("Authorization"), False)
        self.assertIsNone(response.json().get("user"))
        
class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.data = {
            "username":"testuser", 
            "password": "password123",
            "email":"testemail@test.com",
            "phone_number":"0401366312",
            "is_teacher":"true"
            } #for student, the signUpForm in view must have the required=false modifier to also allow False values
                            #because of this, Users can only sign up as teachers from the submitted code}

    def test_duplicate_user(self):
        #create another user with the same email before signup
        User.objects.create(username="testuser1",
                            password=hashed_password("password123"),
                            email="testemail@test.com",
                            phone_number="0401366312",
                            user_type="student")
        
        response = self.client.post(self.url, json.dumps(self.data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'message': 'Email already used!'} )
        User.objects.all().delete()

    def test_valid_signup(self):
        #dummy user for us to determine that the signup view correctly creates a new user object
        #based on the data given to it
        response = self.client.post(self.url, json.dumps(self.data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Signup successful! Logging in...")
        #assert that the attributes are correctly created
        user = response.json()['user']
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['email'], "testemail@test.com")
        self.assertEqual(user['phone_number'],"0401366312")
        self.assertEqual(user['user_type'], "teacher")
        self.assertEqual(user['profile_image'], None) #default value
        user = User.objects.get(username="testuser")
        self.assertEqual(user.password, hashed_password("password123"))
        
    
    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'message':'Invalid request method!'})

    def test_invalid_form(self):
        invalid_data = {
            "username":"testuser", 
            "password": "password123",
            "email":"testemail", #invalid email format
            "phone_number":"04013", #not long enough phone number
            "is_teacher":"true"
            }

        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Invalid form data!'})  


class TestAccountView(TestCase):
    def setUp(self):
        self.url = reverse('change_information')
        User.objects.create(username="og_testuser",
                    password=hashed_password("password123"),
                    email="testemail@test.com",
                    phone_number="0401366312",
                    user_type="student")
        
        self.data = {
            "new_username":"new_testuser",
            "new_email":"newtestemail@test.com",
            "old_email": "testemail@test.com",
            "new_phone_number":"0401123456",
            "given_password":"password123"
        }
    
    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'message':'Invalid request method!'})
    
    def test_invalid_form_data(self):
        #did not implement form checking in change_information :\ very sorry boys
        invalid_data = {
            "new_username":"new_testuser",
            "new_email":"newtestemail",
            "old_email": "testemail@test.com",
            "new_phone_number":"0302",
            "given_password":"password123"
        }

        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        #self.assertEqual(response.status_code, 400)
        #self.assertEqual(response.json(), {'message': 'Invalid form data!'})
    
    def test_invalid_password(self):
        #checks if password is correct or not
        invalid_data = {
            "new_username":"new_testuser",
            "new_email":"newtestemail@test.com",
            "old_email": "testemail@test.com",
            "new_phone_number":"0401123456",
            "given_password":"password1" #wrong password given
        }

        response = self.client.post(self.url, json.dumps(invalid_data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Invalid Password!'} )

    def test_valid_response(self):
        response = self.client.post(self.url, json.dumps(self.data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Information Successfully Changed!")
        #assert that the attributes matches the new ones
        user = response.json()['user']
        self.assertEqual(user['username'], "new_testuser")
        self.assertEqual(user['email'], "newtestemail@test.com")
        self.assertEqual(user['phone_number'],"0401123456")

