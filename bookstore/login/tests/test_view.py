from .test_setup import TestSetUp
from django.urls import reverse

class TestViews(TestSetUp):

    def test_given_valid_id_and_pass_when_correct_returns_respose_200(self):
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)

    # def test_given_valid_id_and_pass_when_correct_returns_respose_200(self):
    #     res = self.client.post(self.login_url, self.wrong_data, format="json")
    #     self.assertEqual(res.status_code, 401)

