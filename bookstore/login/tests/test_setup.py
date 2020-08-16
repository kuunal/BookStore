from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.user_data={
            'login_id':'kunaldeshmukh2503@gmail.com',  
            'password':'Kunal@123'
        }
        self.wrong_data={
            'login_id':9232132222,  
            'password':'wrong@123'
        }
        res = self.client.post(self.login_url, self.user_data, format='json')
        import pdb 
        pdb.set_trace()
        otp = res.data['otp']
        res = self.client.post(reverse('otp'),{'otp':otp})
        self.jwt = res.data['jwt']
        return super().setUp()

    def tearDown(self):
        return super().tearDown()