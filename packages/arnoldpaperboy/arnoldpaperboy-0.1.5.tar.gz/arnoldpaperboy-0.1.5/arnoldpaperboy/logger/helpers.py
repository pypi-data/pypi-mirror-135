# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.rst.
"""stackdriver logging related helper functions
"""
from datetime import timedelta
from functools import wraps
import inspect
import logging
from logging import LoggerAdapter
import os
import time
from timeit import default_timer

from arnoldpaperboy.logger.handlers import MAGIC_PREFIX
from arnoldpaperboy.monitoring.custom_metrics import send_metric


# the PassingLoggerAdapter class is based on the PassingLoggerAdapter class from
# https://github.com/marrink-lab/vermouth-martinize/blob/master/vermouth/log_helpers.py
# and is Copyright 2018 University of Groningen under the Apache 2.0 license.
# The code here is basically a copy-paste from that, and mainly adapted to pass pylint.
class PassingLoggerAdapter(LoggerAdapter):
    """Helper class that is actually capable of chaining multiple LoggerAdapters.

    Args:
        logger (logging.Logger): the logger to extend
        extra (dict): the extra logging keywords
    """
    def __init__(self, logger, extra=None):
        if extra is None:
            extra = {}
        # These are all set by the logger.setter property. Which
        # super().__init__ calls.
        super().__init__(logger, extra)

    # A LoggerAdapter does not have a manager, but logging.Logger.log needs
    # it to see if logging is enabled.
    @property
    def manager(self):
        """proxy to the logger.manager

        Returns:
            logger.manager: the logger manager
        """
        return self.logger.manager

    @manager.setter
    def manager(self, new_value):
        """Setter for the manager.

        Args:
            new_value (manager): replace the manager with this one
        """
        self.logger.manager = new_value

    def process(self, msg, kwargs):
        """logger.process method that does the right thing with 'extra'.

        Args:
            msg (string): message to log
            kwargs (dict): kwargs to log

        Returns:
            tuple(str, dict): msg, kwargs
        """
        # The documentation is a lie and the original implementation clobbers
        # 'extra' that is set by other LoggerAdapters in the chain.
        # LoggerAdapter's process method is FUBARed, and aliases kwargs and
        # self.extra. And that's all it does. So we do it here by hand to make
        # sure we actually have an 'extra' attribute.
        # It should maybe be noted that generally this method gets executed
        # multiple times, so occasionally self.extra items are very persistent.
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        kwargs['extra'].update(self.extra)
        try:
            # logging.Logger does not have a process.
            msg, kwargs = self.logger.process(msg, kwargs)
        except AttributeError:
            pass
        return msg, kwargs

    def log(self, level, msg, *args, **kwargs):
        """Log something. Pass on the right stuff to the internal logger.

        Args:
            level (logging.LEVEL): the logging level
            msg (string): the message
            *args (list): args
            **kwargs (dict): kwargs
        """
        # Differs from super().log because this calls `self.logger.log` instead
        # of self.logger._log. LoggerAdapters don't have a _log.
        if self.isEnabledFor(level):
            msg, kwargs = self.process(msg, kwargs)
            if isinstance(self.logger, logging.Logger):
                # logging.Logger.log throws a hissy fit if it gets too many
                # kwargs, so leave just the ones known.
                kwargs = {key: val for key, val in kwargs.items()
                          if key in ['level', 'msg', 'exc_info', 'stack_info', 'extra']}
                self.logger._log(level, msg, args, **kwargs)  # pylint: disable=protected-access
            else:
                self.logger.log(level, msg, *args, **kwargs)

    def addHandler(self, *args, **kwargs):  # pylint: disable=invalid-name
        """Proxy for logger.addHandler

        Args:
            *args: args
            **kwargs: kwargs
        """
        self.logger.addHandler(*args, **kwargs)

    def setLevel(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Proxy for logger.setLevel

        Args:
            *args: args
            **kwargs: kwargs
        """
        self.logger.setLevel(*args, **kwargs)


class AnnotatedLogger:
    """Contextmanager to temporary annotate the current global logger with extra kwargs.

    Takes a logger or finds it by name in the call stack, and replaces it with a LoggerAdapter.
    On exit the logger in the call stack will be reset again to it's original state. This enables
    the magic that only the 'logger = logging.getLogger(__name__)' at the top of the file is
    necessary, and an adapted logger can be used in other parts of the code without having to add
    code to either get a new logger or to define logger as global.

    Args:
        logger (str or logging.Logger): the (name of) the global logger to annotate
        kwargs (dict): the extra k:v pairs to attach to the logger
    """

    def __init__(self, logger, **kwargs):
        self.logger = logger
        self.kwargs = kwargs
        self.back = 0
        self.from_frame = None

    def __enter__(self):
        """On entering the context.

        Returns:
            LoggerAdapter: the annotated logger
        """
        frame = None
        if isinstance(self.logger, str):
            frame = inspect.currentframe()
            while frame is not None and self.logger not in frame.f_globals:
                frame = frame.f_back
                self.back += 1
            if frame is not None:
                self.from_frame = self.logger
                self.logger = frame.f_globals[self.logger]
            else:
                # could not find logger by name. Create a new one.
                print("Warning: could not get logger by name. Creating new one.")
                self.logger = logging.getLogger(__name__)

        adapted_logger = PassingLoggerAdapter(self.logger, self.kwargs)

        if self.from_frame:
            frame.f_globals[self.from_frame] = adapted_logger
            del frame

        return adapted_logger

    def __exit__(self, *_):
        if self.from_frame:
            frame = inspect.currentframe()
            while self.back > 0:
                frame = frame.f_back
                self.back -= 1
            frame.f_globals[self.from_frame] = self.logger
            del frame


def autolog(logger_name='logger',
            level=logging.DEBUG,
            log_before=True,
            log_after=True,
            metric=False,
            metric_name=None,
            metric_labels=None):
    """Decorate a function for logging candy.

    Decorator to automatically replace the global logger with an AnnotatedLogger, with all the
    the args and kwargs that the decorated function was called with as annotation to the logger.
    When used with the StackdriverLoggingHandler, these annotations will automatically end up as
    extra key:value pairs in the 'labels' section.
    Use the log_before and log_after options to automatically log a starting and a finished message,
    including the time the decorated function took to execute.


    NB. this is not thread-safe! It temporary changes the global scope of the decorated function; if
    from another thread a function (or class) from the same global scope is called, it will see the
    same modification. If we are going to use this in a threaded environment, we should use
    something a bit more extensive like https://github.com/erikrose/stackful.

    Args:
        logger_name (str): the (variable) name of the global logger to use
        level (int): the log level to use for the log_before and log_after messages
        log_before (bool): if True, log a message just before starting the decorated function
        log_after (bool): if True, log a message right after the decorated function finished, using
            a logger annotated with a 'duration' attribute.
        metric (bool): if True, the call duration will be sent as custom metric to stackdriver
            monitoring
        metric_name (str): the name of the custom metric
        metric_labels (list(str)): names of the labels to attach to metric (max = 10)

    Returns:
        function: the decorator.
    """

    def decorator(function):
        """The decorator

        Args:
            function (function): the function to decorate

        Returns:
            function: the function wrapper.
        """

        @wraps(function)
        def wrapper(*args, **kwargs):
            """The function wrapper.

            Args:
                args (list): decorated function args
                kwargs (dict): decorated function kwargs

            Returns:
                result: the result of the decorated function call
            """
            func_fullname = ".".join([function.__module__, function.__qualname__])
            func_file = inspect.getsourcefile(function)
            func_sig = inspect.signature(function)
            bound_args = func_sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            logger_extra = {'arg_{}'.format(k): v for k, v in bound_args.arguments.items()}
            func_kwargs = logger_extra.pop('arg_kwargs', {})
            for key, value in func_kwargs.items():
                logger_extra['arg_{}'.format(key)] = value

            # override some of the logrecord attributes, otherwise these will become references to
            # this decorator instead of the decorated function when logging before and after.
            # Prepend magic prefix to avoid name clashes.
            overrides = dict(
                funcName=func_fullname,
                filename=os.path.basename(func_file),
                module=inspect.getmodule(function).__name__,
                name=function.__name__,
                pathname=func_file,
                lineno=inspect.getsourcelines(function)[-1]
            )
            overrides_prefixed = {'{}{}'.format(MAGIC_PREFIX, k): v for k, v in overrides.items()}

            with AnnotatedLogger(logger_name, **logger_extra) as alogger:

                if log_before:
                    alogger.log(level, "Starting %s", func_fullname, extra=overrides_prefixed)

                start = default_timer()

                result = function(*args, **kwargs)

                end = default_timer()
                timestamp = time.time()
                duration_seconds = end - start

                if log_after:
                    duration_timedelta = timedelta(seconds=duration_seconds)
                    overrides.update(
                        {
                            'duration': duration_timedelta,
                            'duration_seconds': duration_seconds,
                        }
                    )
                    alogger.log(
                        level,
                        "Finished %s in %s", func_fullname, duration_timedelta,
                        extra=overrides_prefixed,
                    )
            if metric:
                custom_metric_name = (
                    metric_name if metric_name else '{}.duration'.format(func_fullname)
                )
                if metric_labels:
                    labels = {
                        k: v for k, v in {**logger_extra, **overrides}.items()
                        if k in metric_labels
                    }
                else:
                    labels = {
                        k: v for k, v in {**logger_extra, **overrides}.items()
                        if k.startswith('arg_')
                    }
                # google does not allow >10 labels on custom metrics
                if len(labels) > 10:
                    labels_split = {}
                    while labels and (len(labels_split) <= 10):
                        labels_split.update([labels.popitem()])
                    if labels:
                        labels.update([labels_split.popitem()])
                        labels_split['truncated_args'] = ' '.join(
                            ['{}: {};'.format(k, v) for k, v in labels.items()]
                        )
                send_metric(
                    custom_metric_name,
                    duration_seconds,
                    labels=labels,
                    timestamp=timestamp,
                )

            return result

        return wrapper

    return decorator
