# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from functools import wraps
import json
import logging
import os
from logging.config import dictConfig

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)

dictConfig(config['logging'])

logger = logging.getLogger()


class LoggerAdapterObserver(object):
    def on_begin_process(self, msg, kwargs):
        pass

    def on_end_process(self, msg, kwargs):
        pass


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger_, extra=None, observer=None):
        super(LoggerAdapter, self).__init__(logger_, extra or {})
        self.prefix = None
        self.replace_handler = None
        self.observer = observer

    def process(self, msg, kwargs):
        if self.observer:
            self.observer.on_begin_process(msg, kwargs)
        if self.replace_handler:
            handlers_copy = self.logger.handlers[:]
            for handler in handlers_copy:
                if isinstance(self.replace_handler, type(handler)):
                    self.logger.removeHandler(handler)
                    self.logger.addHandler(self.replace_handler)
        msg, kwargs = super(LoggerAdapter, self).process(msg, kwargs)
        if self.observer:
            self.observer.on_end_process(msg, kwargs)
        return (
            '%s %s' % (self.prefix, msg) if self.prefix else msg,
            kwargs
        )

    def setLevel(self, level):
        self.logger.setLevel(level)


def function_log(func):
    # noinspection PyShadowingNames
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger.debug('Entering: %s', func.__name__)
        logger.debug('Function params: {} {}'.format(args, kwargs))
        result = func(self, *args, **kwargs)
        logger.debug(u'Function `{}.{}` return: {}'
                     .format(self.__class__.__name__, func.__name__, result))
        return result
    return wrapper
