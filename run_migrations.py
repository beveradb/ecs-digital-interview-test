import logging
import os
import pprint
import re
import sys
import types

import click
import click_log
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
        if level in self.colors:
            prefix += click.style('{}: '.format(level),
                                  **self.colors[level])

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

    logger.debug("run_migrations CLI execution start")
    pp = pprint.PrettyPrinter(indent=4)

    migrations = populate_migrations(migrations_directory)
    pp.pprint(migrations)


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
