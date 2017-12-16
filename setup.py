import sys
from setuptools import setup, find_packages

kwargs = {
    # Packages
    'packages': find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    'include_package_data': True,

    # Dependencies
    'install_requires': [
        'django>=1.4,<1.11',
    ],

    'test_suite': 'test_suite',

    # Metadata
    'name': 'django-support-form',
    'version': __import__('supportform').get_version(),
    'author': 'Bhavani Ravi',
    'author_email': 'bhava0895@gmail.com',
    'description': 'Simple support/contact form for your Django app',
    'license': 'BSD',
    'keywords': 'support contact form',
    'url': 'https://github.com/cbmi/django-support-form/',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
    ],
}

setup(**kwargs)
