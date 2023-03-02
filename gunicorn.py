# gunicorn.py
import multiprocessing
import os

if os.environ.get("MODE") == "dev":
    reload = True

bind = "0.0.0.0:8080"

timeout = 300
# errorlog='/log/api.log'
loglevel = os.environ.get("LOG_LEVEL", "INFO").lower()
# capture_output=True

workers = multiprocessing.cpu_count() * 2 + 1
