Installation
============


The Cybercommons framework is a Django Rest Framework API. The API leverages MongoDB to provide a Catalog and Data Store for storing metadata and data within a JSON document database. The API also includes Celery which is an asynchronous task queue/jobs based on distributed message passing.

## Requirements

* Docker
* Docker Compose
    * `pip install docker-compose`
* GNU Make or equivalent

## Installation

1. Clone Repository

    ```sh
    git clone https://github.com/cybercommons/cybercommons.git
    ```

1. Edit values within dc_config/cybercom_config.env
1. Copy secrets_template.env into secrets.env under the same folder and add required credentials into it. 
1. Initialize database and generate internal SSL certs

    ```sh
    make init
    ```    
1. Build and Deploy on local system.

    ```sh
    make build
    make superuser
    make run
    ```

1. Make Django’s static content available. It only needs to be run once or after changing versions of Django.

    ```sh
    make collectstatic
    ```

1. API running http://localhost
    * Admin credentials set from above `make superuser` 

1. Shutdown cybercommons

    ```sh
    make stop
    ```


## cybercommons Installation on servers with a valid domain name.

1. Edit values within dc_config/cybercom_config.env[NGINX_HOST,NOTIFY_EMAIL,NGINX_TEMPLATE(These values must be set).
1. Copy secrets_template.env into secrets.env under the same folder and add required credentials into it.
1. Initialize database and generate internal SSL certs

    ```sh
    make init
    ```

1. Initialize and Get TLS certificates from LetsEncrypt
        
    ```sh
    make init_certbot
    ```

1. Build and Deploy on local system.

    ```sh
    make build
    make superuser
    make run
    ```

1. Make Django's static content available. This only needs to be ran once or after changing versions of Django.

    ```sh
    make collectstatic
    ```

1. API running https://{domain-name-of-server}
    * Admin credentials set from above `make superuser`

1. Shutdown cybercommons

    ```sh
    make stop
    ```

## TODO

1. Integration with Kubernetes
