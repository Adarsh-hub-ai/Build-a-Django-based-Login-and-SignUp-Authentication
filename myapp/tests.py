import json
import re

from django.contrib.auth.hashers import check_password
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import PendingLogin, PendingSignup, SignIn


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class SignupRequestTests(TestCase):
    def test_send_code_requires_name(self):
        response = self.client.post(
            reverse('send_otp'),
            data=json.dumps({'email': 'learner@example.com'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Name is required.')
        self.assertEqual(PendingSignup.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_send_code_valid_request(self):
        response = self.client.post(
            reverse('send_otp'),

            #json.dumps converts python dict to json object
            data=json.dumps({'name': 'Asha', 'email': 'asha@example.com'}),
            content_type='application/json',
        )


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Verification code sent.')

        pending = PendingSignup.objects.get(email='asha@example.com')
        self.assertEqual(pending.name, 'Asha')
        self.assertGreater(pending.expires_at, timezone.now())
        self.assertEqual(self.client.session['pending_signup_email'], 'asha@example.com')

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ['asha@example.com'])
        code_match = re.search(r'\b(\d{6})\b', message.body)
        self.assertIsNotNone(code_match)
        self.assertTrue(check_password(code_match.group(1), pending.otp_hash))


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class LoginOtpRequestTests(TestCase):
    def setUp(self):
        SignIn.objects.create(name='Asha', email='asha@example.com')

    def test_login_request_sends_code_for_existing_account(self):
        response = self.client.post(
            reverse('login'),
            data=json.dumps({'email': 'asha@example.com'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Verification code sent.')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['asha@example.com'])
        self.assertEqual(self.client.session['pending_login_email'], 'asha@example.com')

        pending = PendingLogin.objects.get(email='asha@example.com')
        self.assertGreater(pending.expires_at, timezone.now())
        self.assertEqual(pending.attempts, 0)
        code_match = re.search(r'\b(\d{6})\b', mail.outbox[0].body)
        self.assertIsNotNone(code_match)
        self.assertTrue(check_password(code_match.group(1), pending.otp_hash))

