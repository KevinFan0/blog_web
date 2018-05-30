#! /usr/bin/env python
# coding=utf-8
import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = '0.0.0.0:5000'

path_of_current_file = os.path.abspath(__file__)
path_of_current_dir = os.path.split(path_of_current_file)[0]


#启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

access_log_format = '{"remote_ip":"%(h)s","request_id":"%({X-Request-Id}i)s","response_code":"%(s)s","request_method":"%(m)s","request_path":"%(U)s","request_querystring":"%(q)s","request_timetaken":"%(D)s","response_length":"%(B)s"}'
logconfig = "/home/fandong/fandong/code/blog_web/flaskr/logging.conf"

pidfile = '%s/run/blog.pid' % (path_of_current_dir)
errorlog = '%s/logs/blog_error.log' % (path_of_current_dir)
accesslog = '%s/logs/blog_access.log' % (path_of_current_dir)

pythonpath = os.path.join(os.path.split(os.path.realpath(__file__))[0])
x_forwarded_for_header = 'X-FORWARDED-FOR'