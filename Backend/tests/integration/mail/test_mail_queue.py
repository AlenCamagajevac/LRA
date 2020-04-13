from task_queue.tasks.mail_handler import (
    send_confirmation_token,
    send_notification_mail
)
from mail import mail


def test_confirmation_mail(app, celery_worker):
    with mail.record_messages() as outbox:
        send_confirmation_token.delay('test@test.com').get(timeout=10)

        assert len(outbox) == 1
        assert outbox[0].subject == "CBC Clusters account registration"


def test_notification_mail(app, celery_worker):

    with mail.record_messages() as outbox:
        # Given
        emails = ['test@test.com', 'test2@test.com', 'test3@test.com']

        # When
        send_notification_mail.delay(
            emails, "TestTitle", "TestUUID").get(timeout=10)

        # Then
        assert len(outbox) == 3
        assert outbox[0].subject == "New article on CBC Clusters app"
