import smtplib
from threading import Thread
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from .settings import SUPPORT_EMAIL, SUPPORT_EMAIL_SUBJECT, SUPPORT_WAIT_SEND, SAVE_SUPPORT_QUERY
from supportform.models import Support

def send_support_mail(form, **kwargs):
    from_email = form.cleaned_data['email']
    subject = '{0}{1}'.format(settings.EMAIL_SUBJECT_PREFIX,
        form.cleaned_data['subject'])
    t = get_template('supportform/email_body.txt')
    kwargs['message'] = form.cleaned_data['message']
    try:
        send_mail(subject, t.render(kwargs), from_email, [SUPPORT_EMAIL])
        if SAVE_SUPPORT_QUERY:
            # Saves the query if the setting is true
            Support.objects.create(email=from_email,subject=subject,description=kwargs["message"])
        form.sent += 1
    except (smtplib.SMTPException, ConnectionRefusedError):
        form.send_error = True
        ## Always save in case of error
        Support.objects.create(email=from_email,subject=subject,description=kwargs["message"])

    form._send_thread = None


class SupportForm(forms.Form):
    SUPPORT_EMAIL = SUPPORT_EMAIL

    email = forms.EmailField(required=False)
    subject = forms.CharField(initial=SUPPORT_EMAIL_SUBJECT, required=False)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.send_error = False
        self.sent = 0
        self._send_thread = None
        super(SupportForm, self).__init__(*args, **kwargs)

    def clean_subject(self):
        return self.cleaned_data.get('subject') or SUPPORT_EMAIL_SUBJECT

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Use user's email if authenticated
        if self.user and self.user.is_authenticated():
            return self.user.email
        # Require for non-authenticated users
        if not email:
            raise forms.ValidationError('This field is required.')
        return email

    def send(self, wait=SUPPORT_WAIT_SEND, force=False, **kwargs):
        # Sending in a thread,
        if self._send_thread:
            return
        if self.sent and not force:
            return
        # Reset the error flag in case this is called multiple times
        self.send_error = False
        # Add the user if it is not already provided
        kwargs.setdefault('user', self.user)

        if wait:
            send_support_mail(self, **kwargs)
        else:
            self._send_thread = Thread(target=send_support_mail, args=(self,),
                kwargs=kwargs)
            self._send_thread.start()
        return not self.send_error
