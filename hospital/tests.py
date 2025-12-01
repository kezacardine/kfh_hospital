from django.test import TestCase

# Create your tests here.
class SimpleTest(TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)

  from django.test import TestCase
from .models import Patient

class PatientModelTest(TestCase):
    def test_create_patient(self):
        patient = Patient.objects.create(
            first_name="Sylvia",
            last_name="Kabarokore",
            age=25,
            gender="Female"
        )
        self.assertEqual(patient.first_name, "Sylvia")
        self.assertEqual(patient.age, 25)


from django.test import TestCase
from .models import Department

class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        dept = Department.objects.create(name="Cardiology")
        self.assertEqual(dept.name, "Cardiology")



from django.test import TestCase
from django.urls import reverse

class ViewTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


from django.contrib.auth.models import User

class LoginTest(TestCase):
    def test_user_login(self):
        user = User.objects.create_user(username='patient1', password='test1234')
        login = self.client.login(username='patient1', password='test1234')
        self.assertTrue(login)


class EmergencyTest(TestCase):
    def test_emergency_page(self):
        response = self.client.get(reverse('emergency'))
        self.assertEqual(response.status_code, 200)

  
