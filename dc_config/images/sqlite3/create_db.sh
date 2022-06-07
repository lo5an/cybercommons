#!/bin/bash

cat /config/django.sql | sqlite3 /data/db.sqlite3
