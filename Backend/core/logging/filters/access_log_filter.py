from logging import Filter
from flask import request
from flask_jwt_extended import decode_token


class AccessLogFilter(Filter):

    def _get_user_token(self):
        if 'Authorization' in request.headers:
            _, token = request.headers['Authorization'].split(' ')
            decoded_token = decode_token(token, allow_expired=True)

            # TODO: user email not uuid(identity)
            # Email of user can be found in claims
            return decoded_token['identity']

        return 'Anonnymous user'

    def filter(self, record):
        record.remote_addr = request.remote_addr
        record.method = request.method
        record.path = request.path
        record.user = self._get_user_token()
        record.headers = request.headers
        record.body = request.data
        return True
