#!/bin/bash
#
# Backup a Postgresql database into a daily file.
#

BACKUP_DIR=$(pwd)/pg_backup
DAYS_TO_KEEP=14
FILE_SUFFIX=_pg_backup.sql
DATABASE=postplata
USER=postgres

FILE=`date +"%Y%m%d%H%M"`${FILE_SUFFIX}

OUTPUT_FILE=${BACKUP_DIR}/${FILE}

if [ ! -d "$BACKUP_DIR" ]; then
    mkdir $BACKUP_DIR
fi


# do the database backup (dump)
# use this command for a database server on localhost. add other options if need be.
sudo -u ${USER} pg_dump --data-only ${DATABASE} > ${OUTPUT_FILE}

# gzip the mysql database dump file
#gzip $OUTPUT_FILE

# prune old backups
find $BACKUP_DIR -maxdepth 1 -mtime +$DAYS_TO_KEEP -name "*${FILE_SUFFIX}.sql" -exec rm -rf '{}' ';'