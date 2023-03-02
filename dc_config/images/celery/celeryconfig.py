import os
import ssl

# Refer to Celery's configuration documentation for details on these settings.
# https://docs.celeryproject.org/en/stable/userguide/configuration.html


def setBrokerSSL():
    if os.environ.get("BROKER_USE_SSL"):
        return {
            "keyfile": "/ssl/client/key.pem",
            "certfile": "/ssl/client/cert.pem",
            "ca_certs": "/ssl/testca/cacert.pem",
            "cert_reqs": ssl.CERT_REQUIRED,
        }
    else:
        return None


# SETUP BROOKER URI
RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.environ.get("RABBITMQ_DEFAULT_VHOST")
broker_url = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@cybercom_rabbitmq:5671/{RABBITMQ_DEFAULT_VHOST}"
broker_use_ssl = setBrokerSSL()
worker_send_task_events = True
result_expires = None
accept_content = ["json"]

# SETUP MONGO URI
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_HOST = os.environ.get("MONGO_HOST", "cybercom_mongo")
MONGO_PORT = os.environ.get("MONGO_PORT", "27017")
MONGO_CERT_KEY_FILE = os.environ.get("MONGO_CERT_KEY_FILE")
MONGO_CA_FILE = os.environ.get("MONGO_CA_FILE")
MONGO_URI_OVERRIDE = os.environ.get("MONGO_URI_OVERRIDE")
if MONGO_URI_OVERRIDE:
    result_backend = MONGO_URI_OVERRIDE
else:
    result_backend = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?ssl=true&tlsCAFile={MONGO_CA_FILE}&tlsCertificateKeyFile={MONGO_CERT_KEY_FILE}"

# result_backend = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?ssl=true&tlsCAFile={MONGO_CA_FILE}&tlsCertificateKeyFile={MONGO_CERT_KEY_FILE}"

mongodb_backend_settings = {
    "database": os.environ.get("MONGO_DB", "cybercom"),
    "taskmeta_collection": os.environ.get("MONGO_TOMBSTONE_COLLECTION", "tombstone"),
}

imports = tuple(os.environ.get("CELERY_IMPORTS").split(","))
