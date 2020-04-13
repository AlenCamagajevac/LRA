from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from core.errors.invalid_confirmation_token import InvalidConfirmationToken
from flask import current_app as app
from flask import render_template
from flask_mail import Message
from mail import mail


class ConfirmationMailHandler():

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['MAIL_SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=app.config['SALT'],
                max_age=expiration
            )
        except (BadSignature, SignatureExpired):
            raise InvalidConfirmationToken
        return email
