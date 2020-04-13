from flask import current_app as app
from flask import render_template
from flask_mail import Message
from mail import mail
from task_queue.task_queue import celery

from itsdangerous import URLSafeTimedSerializer

from logging import getLogger

log = getLogger(__name__)


@celery.task()
def send_notification_mail(emails, article_title, article_uuid):
    article_url = f"{app.config['ARTICLE_DETAILS_ENDPOINT']}/" + \
            f"{article_uuid}"

    mail_template = render_template(
        'notification_mail.html',
        article_title=article_title,
        article_url=article_url
    )

    # Open mail connection
    with mail.connect() as conn:

        # For each user send mail notification
        for email in emails:

            subject = f'New article on CBC Clusters app'
            msg = Message(
                recipients=[email],
                html=mail_template,
                subject=subject
            )

            log.info(f'Sending notification mail to: {email}')
            conn.send(msg)


@celery.task()
def send_confirmation_token(email):
    log.info(f'Sending confirmation mail to: {email}')

    serializer = URLSafeTimedSerializer(app.config['MAIL_SECRET_KEY'])
    token = serializer.dumps(email, salt=app.config['SALT'])

    # Create URL for confirmation endpoint
    # * This should point to frontend endpoint)
    # * That then sends request to backend to confirm account
    # * And then redirects user to login page (After successfull)
    # * Or has buton for resend confirmation mail (After failed)
    confirmation_url = f"{app.config['MAIL_CONFIRMATION_ENDPOINT']}/" + \
        f"{token}"
    mail_template = render_template(
        'confirmation_mail.html',
        confirm_url=confirmation_url
    )

    msg = Message(
        'CBC Clusters account registration',
        recipients=[email],
        html=mail_template
    )
    mail.send(msg)
