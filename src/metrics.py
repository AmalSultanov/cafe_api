from prometheus_client import Gauge

CPU_USAGE = Gauge(
    'process_cpu_usage',
    'Current CPU usage in percent'
)
MEMORY_USAGE = Gauge(
    'process_memory_usage_bytes',
    'Current memory usage in bytes'
)
