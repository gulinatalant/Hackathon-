from django.core.mail import send_mail


def send_code(email, code):
    send_mail(
        'Verify your email address with Event',
        f'Thank you for registration!'
        f'Activation code: {code}',
        'test@gmail.com',
        [email]
    )

def send_code2(email, code):
    send_mail(
        'Восстановление пароля',
        f'Ваш код подтверждения: {code}',
        'test@gmail.com',
        [email]
       )