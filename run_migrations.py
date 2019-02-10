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
    print('To use this script you need python 2.x! got {}'
          .format(sys.version_info))
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
    logger.debug("Migrations found: {}"
                 .format(len(migrations)))

    db_connection = connect_database(db_host, db_user, db_password, db_name)

    db_version = fetch_current_version(db_connection)
    logger.info("Starting with database version: {}".format(db_version))

    unprocessed = get_unprocessed_migrations(db_version, migrations)

    logger.info("Migrations to be processed: {unprocessed} (out of {total})"
                .format(unprocessed=len(unprocessed), total=len(migrations)))

    db_version, total_processed = process_migrations(
        db_connection,
        db_version,
        unprocessed
    )

    logger.info("Database version now {version} after processing {processed}"
                " migrations. {unprocessed} left unprocessed."
                .format(version=db_version, processed=total_processed,
                        unprocessed=len(unprocessed)))

    db_connection.close()


def apply_migration(db_connection, sql_filename):
    with open(sql_filename) as sql_file:
        cursor = db_connection.cursor()
        cursor.execute(sql_file.read().decode('utf-8'), multi=True)
        cursor.close()


def process_migrations(db_connection, db_version, unprocessed_migrations):
    total_processed = 0
    for version_code, sql_filename in unprocessed_migrations:
        logger.debug("Applying migration: {version} with filename: '{file}'"
                     .format(version=version_code, file=sql_filename))
        try:
            apply_migration(db_connection, sql_filename)
            logger.info(
                "Successfully upgraded database to version: {version} by "
                "executing migration in file: '{file}'".format(
                    version=version_code, file=sql_filename)
            )

            db_version = version_code
            total_processed += 1
        except mariadb.Error as error:
            logger.error("Error while processing migration in file: '{file}': "
                         "{error}".format(file=sql_filename, error=error))
            break
    return db_version, total_processed


def get_unprocessed_migrations(db_version, migrations):
    return filter(lambda tup: tup[0] > db_version, migrations)


def fetch_current_version(db_connection):
    current_db_version = 0
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT version FROM versionTable LIMIT 1")
        current_db_version = cursor.fetchone()[0]
        cursor.close()
    except mariadb.Error as error:
        logger.error(
            "Error while attempting to find current database version, assuming"
            " version 0: {}".format(error)
        )
    return current_db_version


def connect_database(host, user, password, name):
    try:
        logger.debug("Attempting to connect to database with details: "
                     "user={user}, password={password}, host={host}, db={db}"
                     .format(user=user, password=password, host=host, db=name))

        db_connection = mariadb.connect(user=user,
                                        password=password,
                                        host=host,
                                        database=name)
        return db_connection

    except mariadb.Error as error:
        logger.error("Database connection error: {}".format(error))
        sys.exit(1)


def sort_migrations(migrations):
    migrations.sort(key=lambda tup: tup[0])


def extract_sequence_num(filename):
    sequence_num = re.search('([0-9]+)[^0-9].+', filename).group(1)
    return int(sequence_num)


def append_migration_to_list(migrations, filename):
    try:
        migrations.append((extract_sequence_num(filename), filename))
    except AttributeError:
        print_error_help_exit("Invalid filename found: {}".format(filename))


def find_migrations_in_directory(migrations, migrations_directory):
    for filename in os.listdir(migrations_directory):
        if filename.endswith(".sql"):
            append_migration_to_list(
                migrations,
                os.path.join(migrations_directory, filename)
            )


def populate_migrations(migrations_directory):
    migrations = []
    find_migrations_in_directory(migrations, migrations_directory)
    sort_migrations(migrations)
    return migrations


# Despite using setuptools to provide entry point, retain option for someone
# to also execute this script directly, for convenience.
if __name__ == "__main__":
    cli()
