from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import SignIn, PendingSignup, PendingLogin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import json
import re
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
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        if not isinstance(data, dict):
            return JsonResponse({'error': 'Expected a JSON object.'}, status=400)

        email = data.get('email')
        if not isinstance(email, str) or not email.strip():
            return JsonResponse({'error': 'Email is required.'}, status=400)
        email = email.strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

        if not SignIn.objects.filter(email__iexact=email).exists():
            return JsonResponse({'error': 'No account exists for this email.'}, status=404)

        otp = str(secrets.randbelow(900000) + 100000)
        try:
            send_mail(
                subject='Your PyLearn login code',
                message=f'Your PyLearn login code is {otp}. It expires in 5 minutes.',
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            return JsonResponse({'error': 'Unable to send the login code. Please try again.'}, status=503)

        PendingLogin.objects.update_or_create(
            email=email,
            defaults={
                'otp_hash': make_password(otp),
                'expires_at': timezone.now() + timedelta(minutes=5),
                'attempts': 0,
            },
        )
        request.session['pending_login_email'] = email
        return JsonResponse({'message': 'Verification code sent.'})

    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

    return render(request, 'myapp/logIn.html')


@ensure_csrf_cookie
@require_GET
def signin(request):
    return render(request, 'myapp/signIn.html')


def sendotp(request):
    if not request.session.get('pending_signup_email'):
        return redirect('signin')
    return render(request, 'myapp/sendcode.html')


@require_POST
def send_otp(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'error': 'Expected a JSON object.'}, status=400)

    is_resend = data.get('resend') is True
    pending_email = request.session.get('pending_signup_email')
    if is_resend:
        if not pending_email:
            return JsonResponse({'error': 'Start signup before requesting a code.'}, status=400)
        pending = PendingSignup.objects.filter(email=pending_email).first()
        if pending is None:
            request.session.pop('pending_signup_email', None)
            return JsonResponse({'error': 'Signup expired. Start again.'}, status=400)
        name, email = pending.name, pending.email

    else:
        name = data.get('name')
        email = data.get('email')
        if not isinstance(name, str) or not name.strip():
            return JsonResponse({'error': 'Name is required.'}, status=400)
        name = name.strip()
        if len(name) > 250:
            return JsonResponse({'error': 'Name must be 250 characters or fewer.'}, status=400)
        if not isinstance(email, str):
            return JsonResponse({'error': 'A valid email address is required.'}, status=400)
        email = email.strip().lower()
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

        if SignIn.objects.filter(email__iexact=email).exists():
            return JsonResponse({'error': 'Email already exists.'}, status=409)

    otp = str(secrets.randbelow(900000) + 100000)
    pending, _ = PendingSignup.objects.update_or_create(
        email=email,
        defaults={
            'name': name,
            'otp_hash': make_password(otp),
            'expires_at': timezone.now() + timedelta(minutes=5),
            'attempts': 0,
        },
    )
    try:
        send_mail(
            subject='Your PyLearn verification code',
            message=f'Your PyLearn verification code is {otp}. It expires in 5 minutes.',
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception:
        return JsonResponse({'error': 'Unable to send the verification email. Please try again.'}, status=503)

    request.session['pending_signup_email'] = pending.email
    return JsonResponse({'message': 'Verification code sent.'})


@require_POST
def verify_otp(request):
    email = request.session.get('pending_signup_email')
    if not email:
        return JsonResponse({'error': 'Start signup before verifying a code.'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({'error': 'Expected a JSON object.'}, status=400)

    code = data.get('code')
    if not isinstance(code, str) or not re.fullmatch(r'\d{6}', code):
        return JsonResponse({'error': 'Enter the 6-digit verification code.'}, status=400)

    pending = PendingSignup.objects.filter(email=email).first()
    if pending is None:
        request.session.pop('pending_signup_email', None)
        return JsonResponse({'error': 'Signup expired. Start again.'}, status=400)

    if pending.expires_at <= timezone.now():
        pending.delete()
        request.session.pop('pending_signup_email', None)
        return JsonResponse({'error': 'Code expired. Start signup again.'}, status=400)

    if pending.attempts >= 5:
        pending.delete()
        request.session.pop('pending_signup_email', None)
        return JsonResponse({'error': 'Too many incorrect attempts. Start signup again.'}, status=429)

    if not check_password(code, pending.otp_hash):
        pending.attempts += 1
        pending.save(update_fields=['attempts'])
        return JsonResponse({'error': 'Incorrect verification code.'}, status=400)

    with transaction.atomic():
        if SignIn.objects.filter(email__iexact=pending.email).exists():
            pending.delete()
            request.session.pop('pending_signup_email', None)
            return JsonResponse({'error': 'An account with this email already exists.'}, status=409)
        SignIn.objects.create(name=pending.name, email=pending.email)
        pending.delete()

    request.session.pop('pending_signup_email', None)
    return JsonResponse({'message': 'Email verified. Signup complete.'})


@require_POST
def verify_login_otp(request):
    email = request.session.get('pending_login_email')
    if not email:
        return JsonResponse({
            'error' : 'Start login again. Session expired'
        }, status = 400) 

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse({
            'error' : 'Invalid Json'
        }, status = 400)

    if not isinstance(data, dict):
        return JsonResponse({
            'error' : 'Expected a Json object'
        }, status= 400)

    code = data.get('code')
    if not isinstance(code, str) or not re.fullmatch(r'\d{6}', code):
        return JsonResponse({
            'error' : 'Enter the 6-digit verification code'
        }, status = 400)

    pending = PendingLogin.objects.filter(email= email).first()
    if pending is None:
        request.session.pop('pending_login_email', None)
        return JsonResponse({
            'error' : 'Login code not found. Start login again.'
        }, status = 400)

    if pending.expires_at <= timezone.now():
        pending.delete()
        request.session.pop('pending_login_email', None)
        return JsonResponse({
            'error' : 'Code expired, resend the code'
        }, status= 400)

    if pending.attempts >= 5:
        pending.delete()
        request.session.pop('pending_login_email', None)
        return JsonResponse({
            'error' : 'Too many unsuccessfull attempts'
        }, status = 400)

    if not check_password(code, pending.otp_hash):
        pending.attempts += 1
        pending.save(update_fields=['attempts'])
        return JsonResponse({
            'error' : 'Incorrect verification code'
        }, status= 400)

    account = SignIn.objects.filter(email__iexact=email).first()
    if account is None:
        pending.delete()
        request.session.pop('pending_login_email', None)
        return JsonResponse({'error': 'Account not found. Start login again.'}, status=400)

    pending.delete()
    request.session.cycle_key()
    request.session.pop('pending_login_email', None)
    # SignIn is a project-specific model, not Django's auth User model.
    # Store the authenticated identity in the session for PyLearn to use.
    request.session['user_email'] = account.email
    return JsonResponse({'message': 'Login successful.'})
