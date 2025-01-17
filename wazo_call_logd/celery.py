# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import multiprocessing

from celery import Celery
from xivo.status import Status

app = Celery()

logger = logging.getLogger(__name__)

WORKER_NAME = 'call-logd'


def configure(config):
    app.conf.accept_content = ['json']
    app.conf.broker_url = config['celery']['broker']
    app.conf.task_default_exchange = config['celery']['exchange_name']
    app.conf.task_default_queue = config['celery']['queue_name']
    app.conf.task_ignore_result = True
    app.conf.task_serializer = 'json'
    app.conf.worker_hijack_root_logger = False
    app.conf.worker_loglevel = logging.getLevelName(config['log_level']).upper()

    app.conf.worker_max_tasks_per_child = 1000
    app.conf.worker_max_memory_per_child = 100000


def spawn_workers(config):
    logger.debug('Starting Celery workers...')
    argv = [
        'call-logd-worker',  # argv[0] is arbitrary
        # NOTE(sileht): setproctitle must be installed to have the celery
        # process well named like:
        #   celeryd: call-logd@<hostname>:MainProcess
        #   celeryd: call-logd@<hostname>:Worker-*
        '--loglevel',
        logging.getLevelName(config['log_level']).upper(),
        '--hostname',
        f'{WORKER_NAME}@%h',
        '--autoscale',
        "{},{}".format(config['celery']['worker_max'], config['celery']['worker_min']),
        '--pidfile',
        config['celery']['worker_pid_file'],
    ]
    process = multiprocessing.Process(target=app.worker_main, args=(argv,))
    process.start()
    return process


def provide_status(status):
    try:
        app.broker_connection().ensure_connection(timeout=1).close()
    except Exception as e:
        logger.debug('Error while connecting to RabbitMQ: %s: %s', type(e).__name__, e)
        status['task_queue']['status'] = Status.fail
        return

    try:
        workers_status = app.control.inspect().ping()
    except Exception as e:
        logger.debug('Error while querying Celery workers: %s: %s', type(e).__name__, e)
        status['task_queue']['status'] = Status.fail
        return

    if not workers_status:
        status['task_queue']['status'] = Status.fail
        return

    logger.debug('Celery workers status: %s', workers_status)

    ok = any(
        worker_name.startswith(WORKER_NAME) and worker_status.get('ok') == 'pong'
        for worker_name, worker_status in workers_status.items()
    )
    status['task_queue']['status'] = Status.ok if ok else Status.fail
