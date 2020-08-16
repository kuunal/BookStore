from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.user_data={
            'login_id':9004546038,  
            'password':'Kunal@123'
        }
        self.wrong_data={
            'login_id':'wrong',  
            'password':'wrong@123'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()