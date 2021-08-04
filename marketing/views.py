from newsletter.settings import MAILCHIMP_API_KEY, MAILCHIMP_EMAIL_LIST_ID
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from .forms import EmailSignupForm
from .models import Signup

import requests
import json

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

mailchimp_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0/'
member_endpoints = f'{mailchimp_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'


def index(request):
    form = EmailSignupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.instance.email
            email_signup_qs = Signup.objects.filter(email=email)
            if email_signup_qs.exists():
                messages.info(request, 'You already subcribed, thanks though')
            else:
                subcribe(email)
                form.save()
                messages.info(
                    request, 'You have subcribed, now you be charged 50$ per month...')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, "index.html", {'form': form})


def subcribe(email):
    payload = {
        'email_address': email,
        'status': 'subscribed'
    }
    payload = json.dumps(payload)

    r = requests.post(
        member_endpoints,
        payload,
        auth=('Hello There', MAILCHIMP_API_KEY)
    )

    return r.status_code, r.json()
