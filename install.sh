#!/bin/bash
#
# install script for daocitemdb - copies files to installation place
#

PYTHON=/usr/bin/python
INSTALL_DIR=/var/www/daocitemdb
DB_DIR=/var/db/daocitemdb

# copy system files
mkdir -p $INSTALL_DIR
cp -R * $INSTALL_DIR

# make an empty database
#mkdir -p $DB_DIR
#touch $DB_DIR/daocitemdb.sqlite3
#chown apache $DB_DIR/daocitemdb.sqlite3
#chmod 664 $DB_DIR/daocitemdb.sqlite3

# set up the database
#$PYTHON $INSTALL_DIR/manage.py syncdb
