# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.rst.
"""Common logging and monitoring utils
"""
import logging
import time

from google.api_core.exceptions import InvalidArgument
from google.cloud import monitoring_v3
from google.cloud.exceptions import NotFound

from arnoldpaperboy.utils.resource import (
    MONITORING_CLIENT, PROJECT_ID, monitoring_resource, stringify_label
)


logger = logging.getLogger(__name__)


def get_or_create_custom_metric_descriptor(client, project_name, name, description='',
                                           display_name=''):
    """Make sure a metric descriptor exists, create it if necessary

    Args:
        client (monitoring_v3.MetricServiceClient): the client
        project_name (string): the gcp project name
        name (string): the metric name
        description (string): the metric description
        display_name (string): the metric display name

    Returns:
        bool: True on success
    """
    metric_descriptor_path = '{}/metricDescriptors/{}'.format(project_name, name)
    logger.debug('Get or create MetricDescriptor: %s', metric_descriptor_path)
    try:
        client.get_metric_descriptor(metric_descriptor_path)
        return True
    except NotFound:
        descriptor = monitoring_v3.types.MetricDescriptor()
        descriptor.type = name
        descriptor.metric_kind = monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE
        descriptor.value_type = monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE
        descriptor.unit = 's'
        if description:
            descriptor.description = description
        if display_name:
            descriptor.display_name = display_name

        client.create_metric_descriptor(project_name, descriptor)
        return True


def send_metric(name,
                value,
                labels=None,
                timestamp=None,
                project=None,
                description='',
                display_name=''):
    """Send a metric (value) to a certain metricDescriptor. Creates the metricDescriptor when
    necessary.

    NB. sending many values in rapid succession is not really supported by google's monitoring
    service. It might be a better idea in that case to use something based on prometheus and
    grafana, or something else.

    Args:
        name (string): name of the metricDescriptor
        value (float): value to send
        labels (dict): labels to add to the metric
        timestamp (float): timestamp, the result of time.time() will do.
        project (string): gcp project name
        description (string): description for the metricDescriptor
        display_name (string): display name for the metricDescriptor
    """
    if not project:
        project = PROJECT_ID
    project_name = MONITORING_CLIENT.project_path(project)
    if not name.startswith('custom.googleapis.com/'):
        name = 'custom.googleapis.com/{}'.format(name)

    get_or_create_custom_metric_descriptor(
        MONITORING_CLIENT, project_name, name, description=description, display_name=display_name
    )

    series = monitoring_v3.types.TimeSeries()

    series.metric.type = name
    if labels:
        labels = {k:stringify_label(v) for k, v in labels.items()}
        series.metric.labels.update(labels)
    resource = monitoring_resource()
    series.resource.type = resource['type']
    series.resource.labels.update(resource['labels'])
    point = series.points.add()
    point.value.double_value = value
    if not timestamp:
        timestamp = time.time()
    point.interval.end_time.seconds = int(timestamp)
    point.interval.end_time.nanos = int(
        (timestamp - point.interval.end_time.seconds) * 10 ** 9)

    try:
        MONITORING_CLIENT.create_time_series(None, name=project_name, time_series=[series])
        print('sent metric {}: {} [{}, {}]'.format(name, value, project, resource['type']))
    except InvalidArgument as exc:
        logger.critical('Sending metric %s failed with %s: %s', name, type(exc), str(exc))
