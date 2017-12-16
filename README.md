# django-support-form

[Forked from PyPi package django-support-form](https://github.com/chop-dbhi/django-support-form)

Simple contact/support form for Django apps.

## What's new
1. Django 1.11 support
2. Model support to save support details

## Setup

Run `python setup.py install` to install the django package

Add `supportform` to `INSTALLED_APPS` along with the following Django contrib apps:

```python
INSTALLED_APPS = (
    'supportform',
    ...
)
```

Include the `supportform.urls` in the the `ROOT_URLCONF`:

```python
from django.conf.urls import url, include

urlpatterns =
[    
    url(r'^support/', include('supportform.urls')),
    ...
]
```

## Settings

- `SUPPORT_EMAIL` - The recipient email address the support email will be sent to, e.g. 'support@example.com'. Default is `DEFAULT_FROM_EMAIL` Django setting.

- `SUPPORT_EMAIL_SUBJECT` - Default email subject prepopulated in the support form. Default is 'Support Message'.

- `SUPPORT_WAIT_SEND` - Wait until the email successfully sends. If set to false, the email will be sent in the background (via a thread). Default `True`

- `SAVE_SUPPORT_QUERY` - Saves support message to DB. Default `False`

## Templates

The templates that come with the django-supportform are functional, but _very_ minimal:

- `supportform/form.html` - Renders the support form omitting the email field is the user is logged in. On submission if the email fails to send, a fallback message will be display to send an email directly to `SUPPORT_EMAIL`.
    - Context received:
        - `form` - `SupportForm` instance
- `supportform/success.html` - Renders a static success/thank you page. This is the page redirected to after successfully sending a message.
    - Context received: (none)

An email template is also provided and can be customized as well:

- `supportform/email_body.txt`
    - Context recieved:
        - `message` - Left by the user
        - `request` - Request object
        - `user` - If the message was left by an authenticated user
