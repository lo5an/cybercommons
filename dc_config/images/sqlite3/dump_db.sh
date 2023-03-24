#!/bin/bash

sqlite3 /data/db.sqlite3 .dump | grep "CREATE TABLE" > /config/django.sql
