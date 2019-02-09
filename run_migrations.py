import logging
import os
import re
import sys
import types

import click
import click_log
import mysql.connector as mariadb
from click_log import ClickHandler

if sys.version_info > (3, 0):
    print("To use this script you need python 2.x! got %s" % sys.version_info)
    sys.exit(1)

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


# Monkey-patch click_log ColorFormatter class format method to add timestamps
def custom_format(self, record):
    if not record.exc_info:
        level = record.levelname.lower()
        msg = record.getMessage()

        prefix = self.formatTime(record, self.datefmt) + " - "
        level_prefix = '{}: '.format(level)
        if level in self.colors:
            level_prefix = click.style(level_prefix, **self.colors[level])
        prefix += level_prefix

        msg = '\n'.join(prefix + x for x in msg.splitlines())
        return msg
    return logging.Formatter.format(self, record)


_default_handler = ClickHandler()
_default_handler.formatter = click_log.ColorFormatter()
_default_handler.formatter.format = types.MethodType(
    custom_format,
    _default_handler.formatter
)

logger.handlers = [_default_handler]


@click.pass_context
def print_error_help_exit(ctx, message):
    logger.error(message)
    click.echo(ctx.get_help())
    sys.exit(1)


@click.group(invoke_without_command=True)
@click_log.simple_verbosity_option(logger, '--loglevel', '-l')
@click.version_option()
@click.pass_context
@click.argument('migrations_directory')
@click.argument('db_user')
@click.argument('db_host')
@click.argument('db_name')
@click.argument('db_password')
def cli(ctx, migrations_directory, db_user, db_host, db_name, db_password):
    """A cli tool for executing SQL migrations in sequence."""

    logger.debug("CLI execution start")
    migrations = populate_migrations(migrations_directory)

    db_connection = connect_database(db_host, db_user, db_password, db_name)
    db_cursor = db_connection.cursor()
    current_db_version = fetch_current_version(db_cursor)


    db_connection.close()


def fetch_current_version(cursor):
    cursor.execute("SELECT version FROM versionTable LIMIT 1")
    current_db_version = cursor.fetchone()

    logger.debug("Current database version: %s" % current_db_version)
    return current_db_version


def connect_database(host, user, password, name):
    try:
        logger.debug("Attempting to connect to database with details: "
                     "user=%s, password=%s, host=%s, database=%s" % (
                         user,
                         password,
                         host,
                         name
                     ))

        db_connection = mariadb.connect(user=user,
                                        password=password,
                                        host=host,
                                        database=name)
        return db_connection

    except mariadb.Error as error:
        logger.error("Database connection error: %s" % error)


def sort_migrations(migrations):
    migrations.sort(key=lambda tup: tup[0])


def extract_sequence_num(filename):
    sequence_num = re.search('([0-9]+)[^0-9].+', filename).group(1)
    return int(sequence_num)


def append_migration_to_list(migrations, filename):
    try:
        migrations.append((extract_sequence_num(filename), filename))
    except AttributeError:
        print_error_help_exit("Invalid filename found: %s" % filename)


def find_migrations_in_directory(migrations, migrations_directory):
    for filename in os.listdir(migrations_directory):
        if filename.endswith(".sql"):
            append_migration_to_list(migrations, filename)


def populate_migrations(migrations_directory):
    migrations = []
    find_migrations_in_directory(migrations, migrations_directory)
    sort_migrations(migrations)
    return migrations


# Despite using setuptools to provide entry point, retain option for someone
# to also execute this script directly, for convenience.
if __name__ == "__main__":
    cli()
