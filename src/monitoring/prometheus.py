import psutil
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import default as default_metrics
from src.core.logging import logger
from src.monitoring.metrics import CPU_USAGE, MEMORY_USAGE
from prometheus_client import REGISTRY, CollectorRegistry, Metric


class AppNameRegistry(CollectorRegistry):
    def collect(self):
        for metric in REGISTRY.collect():
            new_metric = Metric(metric.name, metric.documentation, metric.type)
            for s in metric.samples:
                labels = dict(s.labels)
                labels["app_name"] = "CafeAPI"
                new_metric.add_sample(
                    s.name, value=s.value, labels=labels, timestamp=s.timestamp
                )
            yield new_metric


async def update_system_metrics(info):
    try:
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.Process().memory_info().rss)
    except Exception as e:
        logger.warning(f"Failed to update system metrics: {e}")


def setup_instrumentator(app):
    instrumentator = Instrumentator(
        should_respect_env_var=True, registry=AppNameRegistry()
    )
    instrumentator.add(default_metrics())
    instrumentator.add(update_system_metrics)
    instrumentator.instrument(app).expose(app)
