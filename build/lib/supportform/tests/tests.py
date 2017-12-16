import time
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from supportform.forms import SupportForm


class SupportTestCase(TestCase):
    def test_no_user(self):
        form = SupportForm(None, {'message': 'Help'})
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)

        form = SupportForm(None, {'email': 'foo@bar.com', 'message': 'Help'})
        self.assertTrue(form.is_valid())

    def test_user(self):
        user = User.objects.create_user(username='user', password='root')

        form = SupportForm(user, {'message': 'Help'})
        self.assertTrue(form.is_valid())

    def test_send(self):
        form = SupportForm(None, {'email': 'foo@bar.com', 'message': 'Help'})
        self.assertTrue(form.is_valid())

        # Send and block
        self.assertTrue(form.send())

        # Check outbox and counters
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['webmaster@localhost'])
        self.assertEqual(form.sent, 1)
        self.assertFalse(form.send_error)

        # No redundant sends
        self.assertEqual(form.send(), None)
        self.assertEqual(form.sent, 1)

        # Unless forced..
        self.assertTrue(form.send(force=True))
        self.assertEqual(form.sent, 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].to, ['webmaster@localhost'])

    def test_send_async(self):
        form = SupportForm(None, {'email': 'foo@bar.com', 'message': 'Help'})
        self.assertTrue(form.is_valid())

        # Send in a thread, always returns true
        self.assertTrue(form.send(wait=False))

        # Returns none if already being sent
        self.assertEqual(form.send(), None)

        # Wait for the thread to finish
        time.sleep(1)

        # Ensure it finished
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['webmaster@localhost'])

    def test_form_view(self):
        response = self.client.get(reverse('supportform-form'))
        self.assertContains(response, 'Submit')

    def test_success_view(self):
        response = self.client.get(reverse('supportform-success'))
        self.assertContains(response, 'Thank you')
