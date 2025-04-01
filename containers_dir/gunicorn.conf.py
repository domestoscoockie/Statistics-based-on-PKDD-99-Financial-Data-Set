import multiprocessing
import socket
import fcntl
import struct


workers = multiprocessing.cpu_count() * 2  #classic * 2 + 1 is too much for ec2 t3.micro

bind = "0.0.0.0:8000"
worker_class = 'sync'
timeout = 200

loglevel = 'info'
