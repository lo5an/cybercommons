__author__ = 'cyberCommons Framework'

import os
import ssl
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ****** Application Settings *******************************************************

APPLICATION_TITLE = os.environ.get('APPLICATION_TITLE', 'Cybercommons')

# ******* Backend Communication Celery Brooker and MongoDB **************************

MEMCACHE_HOST = "cybercom_memcache"
MEMCACHE_PORT = 11211

# Celery workers config are setup with the folling DB and Collections
# Change would reqire updating celeryconfig.py within celery image folder
MONGO_DB = os.environ.get('MONGO_DB', "cybercom")
MONGO_LOG_COLLECTION = os.environ.get('MONGO_LOG_COLLECTION', "task_log")
MONGO_TOMBSTONE_COLLECTION = os.environ.get('MONGO_TOMBSTONE_COLLECTION', "tombstone")

SSL_PATH = os.environ.get('SSL_PATH')
RABBITMQ_DEFAULT_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = os.environ.get('RABBITMQ_DEFAULT_PASS')
RABBITMQ_DEFAULT_VHOST = os.environ.get('RABBITMQ_DEFAULT_VHOST')
BROKER_URL = "amqp://{0}:{1}@cybercom_rabbitmq:5671/{2}"
BROKER_URL = BROKER_URL.format(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS, RABBITMQ_DEFAULT_VHOST)
BROKER_USE_SSL = {
    'keyfile': '{0}/client/key.pem'.format(SSL_PATH),
    'certfile': '{0}/client/cert.pem'.format(SSL_PATH),
    'ca_certs': '{0}/testca/cacert.pem'.format(SSL_PATH),
    'cert_reqs': ssl.CERT_REQUIRED
}
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST', 'cybercom_mongo')
MONGO_PORT = os.environ.get('MONGO_PORT', '27017')
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?ssl=true&tlsCAFile={SSL_PATH}/testca/cacert.pem&tlsCertificateKeyFile={SSL_PATH}/client/mongodb.pem"
CELERY_RESULT_BACKEND = MONGO_URI
CELERY_MONGODB_BACKEND_SETTINGS = {
    "database": MONGO_DB,
    "taskmeta_collection": MONGO_TOMBSTONE_COLLECTION
}
# ******* Catalog ******************************************************
CATALOG_EXCLUDE = ['admin', 'config', 'local', 'default_collection', MONGO_DB]
CATALOG_INCLUDE = ['catalog']
CATALOG_URI = MONGO_URI
CATALOG_ANONYMOUS = True
# *********** Data Store ************************************************
DATA_STORE_EXCLUDE = ['admin', 'config', 'local', 'default_collection', MONGO_DB, 'catalog']
DATA_STORE_MONGO_URI = MONGO_URI
DATA_STORE_ANONYMOUS = True

# If you want to enforce perms for SAFE_METHOD
# Set SAFE_METHOD_PERM_REQUIRED Env Variable
# Example: "mydb_mycollection,mydb1_mycollection1"
SAFE_METHOD_PERM_REQUIRED= os.environ.get('SAFE_METHOD_PERM_REQUIRED','').split(',')

# *********** Email Configuration ********************
if os.getenv('EMAIL_HOST'):
    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'false').lower() == 'true'

