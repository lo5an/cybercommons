How To Add Task to Cybercommons
===============================

## Add Task From Remote Version Control (github)
1. Make a copy of [Cybercomq](https://github.com/cybercommons/cybercomq) into your git repo and modify the template for your own task.
    * Update the "name" field in the setup.py file to a unique name (eg: MyUniqueTaskQueue) for your task. This will be used in `CELERY_IMPORTS` section mention below.
    * Any modifications will need to be pushed to your version control repo.
1. Extend the `CELERY_IMPORTS` and `CELERY_SOURCE` values within dc_config/cybercom_config.env
    * Example of `CELERY_IMPORTS` with single import :
    `CELERY_IMPORTS=MyUniqueTaskQueue`
    * Example of `CELERY_IMPORTS` with multiple imports :
    `CELERY_IMPORTS=MyUniqueTaskQueue,MyOtherTaskQueue`

    * `CELERY_SOURCE` should point to a public repository (ex: github or gitlab) url and specify branch if not using default git branch. 
    * Example of `CELERY_SOURCE` with single repo and selecting the `celery5` branch : `CELERY_SOURCE=git+https://github.com/cybercommons/cybercomq@celery5`
    * Example of `CELERY_SOURCE` with multiple repos using their default branches : `CELERY_SOURCE=git+https://github.com/cybercommons/cybercomq,git+https://github.com/cybercommons/emailq`
    * See the following for more pip supported [version control systems](https://pip.pypa.io/en/stable/topics/vcs-support/) to determine their url structure. 
1. To deploy modified task to a running cybercommons instance, the celery container will need to be restarted. The following commands must be ran from the same directory that cybercommons is installed.  
    * To restart just the celery container `docker compose stop cybercom_celery` followed by `docker compose start cybercom_celery`
    * Or to restart all of cybercommons `make stop && make run`

1. To access logs for the celery container and confirm tasks are loaded correctly, run the following command from the same directory that cybercommons is installed
    * `docker compose logs -f cybercom_celery`
1. To interact with your tasks, see the following [instruction](rest_api.html#task-execution-celery) or interact through web browser by vistting [http://localhost/api/queue/](http://localhost/api/queue/)
1. If your task does not show up, clear memcache by navigating to
[http://localhost/api/queue/memcache](http://localhost/api/queue/memcache) as an admin user. If successful, you will see a message indicating `"Memcache": "Cleared"`


