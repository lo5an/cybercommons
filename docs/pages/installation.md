Installation
============


The cyberCommons framework utilizes the [Django Rest Framework](https://www.django-rest-framework.org/) to expose a RESTful API. The API leverages MongoDB to provide a Catalog and Data Store for storing metadata and data within a JSON document database. The API also includes Celery which is an asynchronous task queue/jobs based on distributed message passing.

## Requirements

* [Docker Engine](https://docs.docker.com/engine/install/) or [Docker Desktop](https://docs.docker.com/get-docker/). If you are unsure, we recommend installing Docker Desktop.
* [Docker Compose plugin](https://docs.docker.com/compose/install/#scenario-two-install-the-compose-plugin) if you are not using Docker Desktop.
* GNU Make or equivalent

## Installation

1. Clone Repository

    ```sh
    git clone https://github.com/cybercommons/cybercommons.git
    ```

1. Edit values of environment variables within dc_config/cybercom_config.env. You should not store credentials in this file as it is tracked by version control. 
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

1. Make Django’s static content available. It only needs to be ran once or after changing versions of Django.

    ```sh
    make collectstatic
    ```

1. API running at http://localhost
    * Admin's credentials set from above `make superuser` 

1. Shutdown cybercommons

    ```sh
    make stop
    ```


## cyberCommons Installation on servers with a valid domain name

1. Edit the followig values of environment variables within dc_config/cybercom_config.env
    * `NGINX_HOST=web.example.org`
    * `NGINX_TEMPLATE=letsencrypt`
    
1. Follow the [configuration](configuration.md#configuration-files) instructions to store credentials in the secrets.env file. Edit the following values of environment variables within dc_config/secrets.env
    * `NOTIFY_EMAIL=admin@example.org`

1. Initialize database and generate internal SSL certs

    ```sh
    make init
    ```

1. Initialize and get TLS certificates from LetsEncrypt
        
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

1. API running at https://{domain-name-of-server}
    * Admin's credentials set from above `make superuser`

1. Shutdown cybercommons

    ```sh
    make stop
    ```

## TODO

1. Integration with Kubernetes