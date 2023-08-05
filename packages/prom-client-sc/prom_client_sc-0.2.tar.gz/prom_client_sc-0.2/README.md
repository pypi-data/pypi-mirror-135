# PYTHON-PROMETHEUS-CLIENT

This is thin wrapper over the python prometheus client.

This library simplifies the task of pushing metrics to prometheus pushgateway.

## How to integrate ? 

**Add below line in requirements.txt as a package name**

git+https://{token}@github.com/ShareChat/python-sdk.git@main#egg=prom_client

**Code snippet:** 
```
from python_prom_client import prom_client

// gets the collector Registry that will be used to push metrics to gateway
registry = prom_client.get_registry() 

// This will start background thread to push metrics from above registry to push gateway
pusher = prom_client.Pusher(jobName)


//you can use any kind of metric
g = prom_client.Gauge('metricName', 'Metric description', registry=registry)
g.set_to_current_time()
```
Please refer this link: https://prometheus.io/docs/concepts/metric_types/ for metrics types supported by prometheus

