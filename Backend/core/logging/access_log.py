from logging import getLogger
from core.logging.filters.access_log_filter import AccessLogFilter


log = getLogger('access')
log.addFilter(AccessLogFilter())


def init_access_logger(app):
    @app.after_request
    def after_request_logger(response):
        log.info(
            f'Handled request: ',
            extra={
                'status_code': response.status_code
            })
        return response
