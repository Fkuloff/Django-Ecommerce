from django.core.mail import EmailMessage

from DjangoEcommerce.celery import app


@app.task
def send_email_task(mail_subject, message, email):
    try:
        email_obj = EmailMessage(mail_subject, message, to=[email])
        email_obj.send()
    except Exception as e:
        raise e

# celery -A DjangoEcommerce worker -l INFO --pool=solo

