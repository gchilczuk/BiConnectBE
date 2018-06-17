from django.core.mail import send_mail

from BiConnect import settings


def prepare_address(speech):
    return f'http://localhost:3000/?m={speech.meeting_id}&s={speech.id}'


def prepare_mail_body(speech):
    address = prepare_address(speech)
    return f'Na spotkaniu w dniu {speech.date} została odnotowana twoja wypowiedź: \n\n {str(speech)} \n\n' \
           f'Swoją wypowiedź możesz potwierdzić lub edytować jeśli masz jakieś uwagi pod adresem: {address} \n' \
           f'Jeżeli nie potwierdzisz wypowiedzi zostanie ona automatycznie potwierdzona po tygodniu od spotkania.'


def prepare_mail_html_body(speech):
    address = prepare_address(speech)
    html_speech = str(speech).replace('\n', '<br/>')
    return f'Na spotkaniu w dniu {speech.date} została odnotowana twoja wypowiedź: <p> {html_speech} </p>' \
           f'<p>Swoją wypowiedź możesz potwierdzić lub edytować jeśli masz jakieś uwagi: ' \
           f'<a href="{address}">tutaj</a>.<br/>' \
           f'Jeżeli nie potwierdzisz wypowiedzi zostanie ona automatycznie potwierdzona po tygodniu od spotkania.</p>'


def send_speechsum_mail(speech):
    if speech.person.email:
        return send_mail(
            subject='Podsumowanie wypowiedzi',
            message=prepare_mail_body(speech),
            html_message=prepare_mail_html_body(speech),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[speech.person.email],
            fail_silently=False,
        )
