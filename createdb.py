
import sys
import logging
import os
from pathlib import Path
import MySQLdb
import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dbhost = ''
dbname = ''
dbuser = ''
dbpass = ''
port = ''


if __name__ == '__main__':

    with open('minhoteca/.env') as f:
        for line in f:
            content = line.split('=')
            os.environ[content[0]] = content[1].strip()

    dbhost = os.getenv('DATABASE_HOST', 'localhost')
    dbname = os.getenv('DATABASE_NAME', 'minhoteca')
    dbuser = os.getenv('DATABASE_USER', 'root')
    dbpass = os.getenv('DATABASE_PASSWORD','123456')
    port = int(os.getenv('DATABASE_PORT', '3306'))

    print(dbhost)

    try:
        db = MySQLdb.connect(
            host=dbhost,
            user=dbuser,
            passwd=dbpass,
            port=port,
            db='mysql',
            connect_timeout=5)
        cur = db.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
        cur.execute(f"GRANT ALL PRIVILEGES ON {dbname}.* TO '{dbuser}'@'%'")
        cur.close()
        print('Database created successfully.')
        sys.exit(0)
    except Exception as ex:
        logger.error(ex)
        sys.exit(1)