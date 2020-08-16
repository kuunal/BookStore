from .test_setup import TestSetUp
from django.urls import reverse

class TestViews(TestSetUp):

    def test_given_valid_id_and_pass_when_correct_returns_respose_200(self):
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

    def test_given_valid_id_and_pass_when_incorrect_returns_respose_401(self):
        res = self.client.post(self.login_url, self.wrong_data, format="json")
        self.assertEqual(res.data['message'], 'invalid Id or pass')

    def test_given_otp_when_valid_returns_json_token(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        otp = res.data['otp']
        res = self.client.post(reverse('otp'),{'otp':otp})
        self.assertEqual(res.data['message'],'Successfully verified')
        self.assertIsNotNone(res.data['jwt'])
        
