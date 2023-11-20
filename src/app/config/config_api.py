"""Config for API."""
from jaeger_client import Config

HOST = '0.0.0.0'  # noqa: S104
PORT = 8000

MAIN_URL = f'http://{HOST}:{PORT}'
NAME_IN_K8S = 'url-shortener'

config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': 'jaeger-agent.monitoring.svc.cluster.local',
            'reporting_port': 6831,
        },
        'logging': True,
    },
    service_name=NAME_IN_K8S,
    validate=True,
)
