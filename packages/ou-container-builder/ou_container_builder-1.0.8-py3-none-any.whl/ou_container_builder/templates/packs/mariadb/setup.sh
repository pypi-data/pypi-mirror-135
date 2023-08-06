#!/bin/bash

service mysql start

sleep 5

# Check if the database exists and if not create it
echo "SHOW SCHEMAS;" | mysql | grep "{{ mariadb.database }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE DATABASE {{ mariadb.database }}" | mysql
fi

# Check if the user exists and if not create it
echo "SELECT user FROM mysql.user;" | mysql | grep "{{ mariadb.username }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE USER {{ mariadb.username }} IDENTIFIED BY '{{ mariadb.password }}';" | mysql
fi

# Grant the user all privileges to the database
echo "GRANT ALL PRIVILEGES ON {{ mariadb.database }}.* TO {{ mariadb.username }};" | mysql

service mysql stop
