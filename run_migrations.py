import logging
import os
import re
import sys
import types

import click
import click_log
import mysql.connector as mariadb
from click_log import ClickHandler

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


@click.command()
@click.argument('sql_directory')
@click.argument('db_user')
@click.argument('db_host')
@click.argument('db_name')
@click.argument('db_password')
@click.option('-s', '--single-file', required=False, type=str,
              help='Filename of single SQL script to process.')
@click_log.simple_verbosity_option(logger, '--loglevel', '-l')
@click.version_option(None, '-v', '--version')
def cli(sql_directory, db_user, db_host, db_name, db_password, single_file):
    """A cli tool for executing SQL migrations in sequence."""

    logger.debug("CLI execution start")
    db_params = (db_host, db_user, db_password, db_name)

    if single_file is not None:
        logger.warning(
            "Use of this option means DB version will be out of sync!"
        )

        apply_migration(db_params, single_file)

        logger.info(
            "Successfully executed SQL in file: '{}'".format(single_file)
        )
        return

    migrations = populate_migrations(sql_directory)
    logger.debug("Migrations found: {}"
                 .format(len(migrations)))

    db_version = fetch_current_version(db_params)
    logger.info("Starting with database version: {}".format(db_version))

    unprocessed = get_unprocessed_migrations(db_version, migrations)

    logger.info(
        "Migrations yet to be processed: {unprocessed} (out of {total} "
        "in dir)".format(
            unprocessed=len(unprocessed),
            total=len(migrations)
        )
    )

    db_version, total_processed = process_migrations(
        db_params,
        db_version,
        unprocessed
    )

    logger.info("Database version now {version} after processing {processed}"
                " migrations. Remaining: {unprocessed}."
                .format(version=db_version, processed=total_processed,
                        unprocessed=(len(unprocessed) - total_processed)))


def apply_migration(db_params, sql_filename):
    with open(sql_filename) as sql_file:
        db_connection = connect_database(db_params)
        cursor = db_connection.cursor()
        cursor.execute(sql_file.read(), multi=True)
        db_connection.close()


def update_current_version(db_params, new_version):
    current_db_version = 0
    try:
        db_connection = connect_database(db_params)
        cursor = db_connection.cursor()
        cursor.execute('UPDATE versionTable SET version = {}'
                       .format(new_version))
        cursor.execute("SELECT version FROM versionTable LIMIT 1")
        db_version_row = cursor.fetchone()
        if db_version_row is not None:
            current_db_version = db_version_row[0]
        db_connection.close()
    except mariadb.Error as error:
        logger.error(
            "Error while attempting to update current database version, "
            "assuming version 0: {}".format(error)
        )
    return current_db_version


def process_migrations(db_params, db_version, unprocessed_migrations):
    total_processed = 0
    for version_code, sql_filename in unprocessed_migrations:
        logger.debug("Applying migration: {version} with filename: '{file}'"
                     .format(version=version_code, file=sql_filename))
        try:
            apply_migration(db_params, sql_filename)
            logger.info(
                "Successfully upgraded database from version: {old} to"
                " {new} by executing migration in file: '{file}'".format(
                    old=db_version, new=version_code, file=sql_filename)
            )

            db_version = update_current_version(db_params, version_code)
            total_processed += 1
        except mariadb.Error as error:
            logger.error("Error while processing migration in file: '{file}': "
                         "{error}".format(file=sql_filename, error=error))
            break
    return db_version, total_processed


def get_unprocessed_migrations(db_version, migrations):
    return [tup for tup in migrations if tup[0] > db_version]


def fetch_current_version(db_params):
    current_db_version = 0
    try:
        db_connection = connect_database(db_params)
        cursor = db_connection.cursor()
        cursor.execute("SELECT version FROM versionTable LIMIT 1")
        current_db_version = int(cursor.fetchone()[0])
        db_connection.close()
    except mariadb.Error as error:
        logger.error(
            "Error while attempting to find current database version, assuming"
            " version 0: {}".format(error)
        )
    return current_db_version


def connect_database(db_params):
    try:
        host, user, password, name = db_params
        logger.debug("Connecting to database with details: "
                     "user={user}, password={password}, host={host}, db={db}"
                     .format(user=user, password=password, host=host, db=name))

        db_connection = mariadb.connect(user=user,
                                        password=password,
                                        host=host,
                                        database=name)
        db_connection.autocommit = True
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
        logger.error("Invalid filename found: {}".format(filename))
        sys.exit(1)


def find_migrations_in_directory(migrations, sql_directory):
    for filename in os.listdir(sql_directory):
        if filename.endswith(".sql"):
            append_migration_to_list(
                migrations,
                os.path.join(sql_directory, filename)
            )


def populate_migrations(sql_directory):
    migrations = []
    find_migrations_in_directory(migrations, sql_directory)
    sort_migrations(migrations)
    return migrations


# Despite using setuptools to provide entry point, retain option for someone
# to also execute this script directly, for convenience.
if __name__ == "__main__":
    cli()
