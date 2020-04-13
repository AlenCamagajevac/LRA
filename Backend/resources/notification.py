from flask_restplus import Namespace, Resource, fields
from flask_jwt_extended import get_jwt_identity
from core.enum.role_enum import RoleTypes
from core.auth.jwt import jwt_required
from core.responses.error_response import ErrorResponse
from dao.user.user import User
from schemas.error.error_response_schema import ErrorResponseSchema
from schemas.user.user_schema import UserSchema
from schemas.user.notification_preferences_schema import (
    NotificationPreferencesSchema)
from logging import getLogger

log = getLogger(__name__)

api = Namespace(
    'notification',
    description='Notification endpoints for CBC Clusters platform')

notification_preferences_model = api.model('Update notification preferences', {
    'allow_mail_notifications': fields.Boolean(
        description='Should user recieve mails'),
    'allow_push_notifications': fields.Boolean(
        description='Should user recieve push notifications')
})


@api.route('')
class NotificationResource(Resource):
    error_schema = ErrorResponseSchema()
    user_schema = UserSchema()
    notification_preferences_schema = NotificationPreferencesSchema()

    @api.expect(notification_preferences_model)
    @api.response(204, 'No Content')
    @jwt_required([RoleTypes.ADMIN, RoleTypes.CLIENT])
    def post(self):
        # Find user
        uuid = get_jwt_identity()
        user = User.find_by_uuid(uuid)
        if not user:
            error_response = self.error_schema.dump(ErrorResponse(
                details={
                    'uuid': f'User with {uuid} uuid does not exist'
                },
                error='User not found'
            ))
            log.info(
                f'User not found: {error_response}')
            return error_response, 404

        # Deserialize input
        notification_preferences = self.notification_preferences_schema.load(
            api.payload)

        # update notification preferences
        for key, value in notification_preferences.items():
            setattr(user, key, value)
        user.commit()

        # return updated user
        return self.user_schema.dump(user), 200
