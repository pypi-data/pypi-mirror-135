#!/bin/bash

service mysql start

sleep 5

echo "SHOW SCHEMAS;" | mysql | grep "{{ mariadb.database }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE DATABASE {{ mariadb.database }}" | mysql
fi

echo "SELECT user FROM mysql.user;" | mysql | grep "{{ mariadb.username }}"
ret=$?
if [ $ret -ne 0 ];
then
  echo "CREATE USER {{ mariadb.username }} IDENTIFIED BY '{{ mariadb.password }}';" | mysql
  echo "GRANT ALL PRIVILEGES ON {{ mariadb.database }}.* TO {{ mariadb.username }};" | mysql
fi

service mysql stop
