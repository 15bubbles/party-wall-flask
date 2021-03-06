import multiprocessing
import os

HOST = os.getenv("HOST", "127.0.0.1")
PORT = os.getenv("PORT", "5000")
ENVIRONMENT = os.getenv("ENVIRONMENT")

bind = f"{HOST}:{PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

daemon = False
proc_name = "party_wall_gunicorn"

loglevel = "info"
# errorlog = ""
# accesslog = ""
# access_log_format = ""


if ENVIRONMENT in ["development", "dev"]:
    workers = 1
    reload = True
