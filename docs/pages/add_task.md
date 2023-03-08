How To Add Task to Cybercommons
===============================

## Add Task From Remote Version Control (git)
1. Make a copy of [Cybercomq](https://github.com/cybercommons/cybercomq) into your git repo and modify the template for your own task.
1. Extend the followig values of environment variables within dc_config/cybercom_config.env
    * `CELERY_IMPORTS` will use the "name" field in the setup.py file of the template task. This should be changed by the user. 
    * `CELERY_SOURCE` should point to a public git repository url (ex: github or gitlab)

