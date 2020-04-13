from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app=None)
# TODO: set version in config and use it here and in api
app_version = metrics.info('app_version', 'Application version')

# Register custom app wide metrics here
app_version.set(0.1)
