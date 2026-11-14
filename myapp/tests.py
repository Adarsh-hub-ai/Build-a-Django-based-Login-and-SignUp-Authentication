import json

from django.test import TestCase
from django.urls import reverse


class SignupRequestTests(TestCase):
    def test_send_code_requires_name(self):
        response = self.client.post(
            reverse('send_otp'),
            data=json.dumps({'email': 'learner@example.com'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Name is required.')

    def test_send_code_valid_request(self):
        response = self.client.post(
            reverse('send_otp'),
            data= json.dumps({"name": "Asha", "email": "asha@example.com"}),
            content_type= 'application/json'
        )



        self.assertEqual(response.status_code, 200)