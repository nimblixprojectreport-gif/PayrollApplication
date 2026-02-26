from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company, Employee, Attendance, Order
from .utils import calculate_distance
from rest_framework.test import APIClient
from django.urls import reverse

class ProximityAssignmentTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name="Tech Corp", email="tech@example.com")
        
        # User 1 and Employee 1 (Near point 0,0)
        self.user1 = User.objects.create_user(username="emp1", password="password")
        self.emp1 = Employee.objects.create(
            company=self.company, user=self.user1, employee_code="E001",
            first_name="Alice", last_name="Smith", email="alice@example.com", mobile="123"
        )
        Attendance.objects.create(employee=self.emp1, latitude=0.0, longitude=0.0)

        # User 2 and Employee 2 (Near point 10,10)
        self.user2 = User.objects.create_user(username="emp2", password="password")
        self.emp2 = Employee.objects.create(
            company=self.company, user=self.user2, employee_code="E002",
            first_name="Bob", last_name="Jones", email="bob@example.com", mobile="456"
        )
        Attendance.objects.create(employee=self.emp2, latitude=10.0, longitude=10.0)

    def test_order_assignment_to_nearest_employee(self):
        # Create an order closer to Alice (emp1) at (0.1, 0.1)
        order1 = Order.objects.create(
            company=self.company, description="Order 1",
            latitude=0.1, longitude=0.1
        )
        
        response = self.client.post(reverse('order-assign'), {'order_id': order1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['employee_id'], self.emp1.id)
        
        # Verify in DB
        order1.refresh_from_db()
        self.assertEqual(order1.assigned_employee, self.emp1)
        self.assertTrue(order1.is_assigned)

    def test_order_assignment_to_bob(self):
        # Create an order closer to Bob (emp2) at (9.9, 9.9)
        order2 = Order.objects.create(
            company=self.company, description="Order 2",
            latitude=9.9, longitude=9.9
        )
        
        response = self.client.post(reverse('order-assign'), {'order_id': order2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['employee_id'], self.emp2.id)
        
        order2.refresh_from_db()
        self.assertEqual(order2.assigned_employee, self.emp2)

    def test_distance_utility(self):
        # Test distance calculation roughly
        # 0,0 to 0.1,0.1 is approx 15.7 km
        dist = calculate_distance(0, 0, 0.1, 0.1)
        self.assertAlmostEqual(dist, 15.7, places=1)
