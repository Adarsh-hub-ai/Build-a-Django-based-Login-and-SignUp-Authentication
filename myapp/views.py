
from django.shortcuts import render
from django.http import JsonResponse
from .models import SignIn, PendingSignup
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import json
import secrets

def index(request):
    return render(request, 'myapp/index.html')


def python(request):
    return render(request, 'myapp/python.html')

@ensure_csrf_cookie
def login(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if 'email' not in data:
                return JsonResponse({
                    'error' : 'Email is required'
                }, status= 400)

            email = data['email']

            if not email:
                return JsonResponse({
                    'error' : 'Email is required'
                }, status= 400)


            user = SignIn.objects.filter(email= email).first()

            if user is None:
                return JsonResponse({
                    'error' : '*User doesnt exists'
                }, status= 404)


        except json.JSONDecodeError:
            return JsonResponse({
                'error' : 'Invalid json'
            }, status= 400)
            

    return render(request, 'myapp/logIn.html')


@ensure_csrf_cookie
def signin(request):

    if request.method == 'POST':
        body = request.body

        try:
            data = json.loads(body)

            if not isinstance(data, dict):
                return JsonResponse({
                    'error' : 'Data needs to be Json'
                }, status= 400)

            name = data['name']
            email = data['email']

            if not name or email is None:
                return JsonResponse({
                    'error' : 'Name and email is needed'
                }, status= 400)

            if 'name' not in data or 'email' not in data:
                return JsonResponse({
                    'error' : 'Name or Email not found'
                }, status= 400)
            
            SignIn.objects.create(
                name = name,
                email = email
            )

        except json.JSONDecodeError:
            return JsonResponse({
                'error' : 'Invalid Json'
            }, status= 400)
        

    return render(request, 'myapp/signIn.html')




def sendotp(request):
    return render(request, 'myapp/sendcode.html')


def send_otp(request):
    otp = str(secrets.randbelow(900000) + 100000)
    hash_otp = make_password(otp)

    if request.method != 'POST':
        return JsonResponse({
            'error' : 'Post required'
        }, status= 405)
        
    try:
        body = request.body
        data = json.loads(body)

        if not isinstance(data, dict):
            return JsonResponse({
                'error' : 'Data needs to be Json'
            }, status= 400)

        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return JsonResponse({
                'error' : 'Name and email needs to be present'
            }, status= 400)

        PendingSignup.objects.create(
            name=  name,
            email= email,
            otp_hash = hash_otp,
            expires_at = timezone.now() + timedelta(minutes= 5)
        )


    
    except json.JSONDecodeError:
        return JsonResponse({
            'error' : 'Invalid Json'
        }, status= 400)



def email_otp(request):
    pass










    






