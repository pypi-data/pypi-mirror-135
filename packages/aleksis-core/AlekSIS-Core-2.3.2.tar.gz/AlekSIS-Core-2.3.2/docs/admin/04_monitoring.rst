Monitoring
##########

Prometheus
**********

AlekSIS provides a metric endpoint at `/metrics`, so you can scrape metrics in
your Prometheus instance.

Available metrics
=================

The exporter provides metrics about responses and requests, e.g.  statistics
about response codes, request latency and requests per view.  It also
provides data about database operations.

Prometheus config to get metrics
================================

To get metrics of your AlekSIS instance, just add the following to your
`prometheus.yml`::

  - job_name: aleksis
    static_configs:
      - targets: ['my.aleksis-instance.com']
    metrics_path: /metrics


Grafana
*******

Visualise metrics with Grafana
==============================

If you want to visualise your AlekSIS metrics with Grafana, you can use one
of the public available Grafana dashboards, for example the following one,
or just write your own.

https://grafana.com/grafana/dashboards/9528
