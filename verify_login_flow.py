import os
import django
from unittest.mock import patch
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Crowdsolve.settings')
django.setup()

with patch('CrowdSolver.views.send_mail') as send_mail_mock:
    client = Client()
    response = client.post('/membersignup/', {
        'membername': 'Test User',
        'membercontact': '9999999999',
        'memberemail': 'testuser@example.com',
        'memberpass': 'Password123!',
        'membercpass': 'Password123!',
        'flatnumber': 'B-101',
        'residentType': 'OWNER',
    }, follow=True)
    print('signup status:', response.status_code)
    print('signup redirects:', response.redirect_chain)
    print('signup length:', len(response.content))
    print('session keys:', list(client.session.keys()))
    otp = client.session.get('otp')
    print('otp stored:', otp)

    if otp:
        response2 = client.post('/verifymember/', {'motp': otp}, follow=True)
        print('verify status:', response2.status_code)
        print('verify redirects:', response2.redirect_chain)
        print('verify length:', len(response2.content))

        response3 = client.post('/memberlogin/', {
            'loginmail': 'testuser@example.com',
            'loginpassword': 'Password123!'
        }, follow=True)
        print('login status:', response3.status_code)
        print('login redirects:', response3.redirect_chain)
        print('login length:', len(response3.content))
    else:
        print('No OTP found; signup may have failed.')
