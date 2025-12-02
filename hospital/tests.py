from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Patient, Department, Vitalsign

# Create your tests here.
class SimpleTest(TestCase):
    def test_example(self):
        self.assertEqual(1 + 1, 2)


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


class DepartmentModelTest(TestCase):
    def test_department_creation(self):
        dept = Department.objects.create(name="Cardiology")
        self.assertEqual(dept.name, "Cardiology")


class ViewTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class LoginTest(TestCase):
    def test_user_login(self):
        user = User.objects.create_user(username='patient1', password='test1234')
        login = self.client.login(username='patient1', password='test1234')
        self.assertTrue(login)


class EmergencyTest(TestCase):
    def test_emergency_page(self):
        response = self.client.get(reverse('emergency'))
        self.assertEqual(response.status_code, 200)


# Put the quick actions test inside a TestCase class
class DashboardQuickActionsTest(TestCase):
    def setUp(self):
        self.client.login(username='admin', password='pass123')  # make sure admin exists or create user before

    def test_quick_actions_links(self):
        response = self.client.get(reverse('hospital:dashboard'))
        self.assertContains(response, reverse('hospital:analytics'))
        self.assertContains(response, reverse('admin:hospital_patient_add'))
        self.assertContains(response, reverse('admin:hospital_vitalsign_add'))


class DashboardContextTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='pass123')
        # Create sample patients
        Patient.objects.create(first_name='John', last_name='Doe', gender='M', phone='123')
        Patient.objects.create(first_name='Jane', last_name='Smith', gender='F', phone='456')
        self.client.login(username='admin', password='pass123')
    
    def test_dashboard_counts(self):
        response = self.client.get(reverse('hospital:dashboard'))
        self.assertEqual(response.context['total_patients'], Patient.objects.count())
