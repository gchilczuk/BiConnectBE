from django.core.mail import send_mail

from BiConnect import settings


def prepare_mail_body(speech):
    return str(speech)


def send_speechsum_mail(speech):
    if speech.person.email:
        return send_mail(
            'Podsumowanie wypowiedzi',
            prepare_mail_body(speech),
            settings.EMAIL_HOST_USER,
            [speech.person.email],
            fail_silently=False,
        )
