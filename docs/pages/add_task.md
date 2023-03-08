How To Add Task to Cybercommons
===============================

## Add Task From Remote Version Control (git)
1. Make a copy of [Cybercomq](https://github.com/cybercommons/cybercomq) into your git repo and modify to your own task.
1. Extend the followig values of environment variables within dc_config/cybercom_config.env
    * `CELERY_IMPORTS=your_task_name`
    * `CELERY_SOURCE=your_task_git_repo`

## Add Task From Local Package
1. Clone [Cybercomq](https://github.com/cybercommons/cybercomq) into local machine and modify packagename and taskname as necessary. 
1. Extend the followig values of environment variables within dc_config/cybercom_config.env
    * `CELERY_IMPORTS=your_task_name`
    * `CELERY_SOURCE=local_package_name`
