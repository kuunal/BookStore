from django.test import TestCase
from rest_framework.test import APITestCase
from login.tests.test_setup import TestSetUp
from django.urls import reverse

# Create your tests here.
class TestView(TestSetUp):
    
    def test_demosssssssssss(self):
        res = self.client.get(reverse('cart'), **{'X_TOKEN':self.jwt})
        import pdb
        pdb.set_trace()
        self.assertEqual(len(res.data),1)