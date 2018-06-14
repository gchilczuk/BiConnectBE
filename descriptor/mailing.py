from django.core.mail import send_mail

from BiConnect import settings


def prepare_mail_body(speech):
    return f'Twoja wypowiedź: \n\n {str(speech)}' \
           f'Jeśli masz jakieś uwagi edytuj swoją wypowiedź tutaj' \
           f'--tutaj link--'


def send_speechsum_mail(speech):
    if speech.person.email:
        return send_mail(
            'Podsumowanie wypowiedzi',
            prepare_mail_body(speech),
            settings.EMAIL_HOST_USER,
            [speech.person.email],
            fail_silently=False,
        )
