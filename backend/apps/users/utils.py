import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_otp_sms(phone_number, otp_code):
    """Send OTP via SMS"""
    try:
        # Implement SMS API integration
        # This is a placeholder - replace with actual SMS service
        message = f"Your Local Delivery App verification code is: {otp_code}. Valid for 10 minutes."
        
        # Example using a generic SMS API
        if settings.SMS_API_KEY and settings.SMS_API_URL:
            payload = {
                'api_key': settings.SMS_API_KEY,
                'phone': phone_number,
                'message': message
            }
            response = requests.post(settings.SMS_API_URL, data=payload)
            return response.status_code == 200
        
        # For development, just print the OTP
        print(f"SMS OTP for {phone_number}: {otp_code}")
        return True
        
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return False


def send_otp_email(email, otp_code):
    """Send OTP via email"""
    try:
        subject = 'Local Delivery App - Verification Code'
        message = f"""
        Your verification code is: {otp_code}
        
        This code will expire in 10 minutes.
        
        If you didn't request this code, please ignore this email.
        
        Best regards,
        Local Delivery App Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


def send_welcome_email(user):
    """Send welcome email to new users"""
    try:
        subject = 'Welcome to Local Delivery App!'
        html_message = render_to_string('emails/welcome.html', {
            'user': user,
            'app_name': 'Local Delivery App'
        })
        
        send_mail(
            subject,
            '',
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
        
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False


def send_password_reset_email(user, reset_token):
    """Send password reset email"""
    try:
        subject = 'Local Delivery App - Password Reset'
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        html_message = render_to_string('emails/password_reset.html', {
            'user': user,
            'reset_url': reset_url,
            'app_name': 'Local Delivery App'
        })
        
        send_mail(
            subject,
            '',
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
        
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False
