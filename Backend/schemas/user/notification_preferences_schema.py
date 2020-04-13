from marshmallow import Schema, fields


class NotificationPreferencesSchema(Schema):
    allow_mail_notifications = fields.Boolean(required=True, load_only=True)
    allow_push_notifications = fields.Boolean(required=True, load_only=True)
