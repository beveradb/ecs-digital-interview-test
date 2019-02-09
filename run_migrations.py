import logging
import sys

import click
import click_log
from click_log import ClickHandler

if sys.version_info > (3, 0):
    print("To use this script you need python 2.x! got %s" % sys.version_info)
    sys.exit(1)


class CustomColorFormatter(click_log.ColorFormatter):
    colors = {
        'error': dict(fg='red'),
        'exception': dict(fg='red'),
        'critical': dict(fg='red'),
        'info': dict(fg='bright_green'),
        'debug': dict(fg='blue'),
        'warning': dict(fg='yellow')
    }

    def format(self, record):
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


logger = logging.getLogger(__name__)
click_log.basic_config(logger)

_default_handler = ClickHandler()
_default_handler.formatter = CustomColorFormatter()

logger.handlers = [_default_handler]


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

    logger.debug("CLI executed, TODO: implement functionality")


@click.pass_context
def print_help_exit(ctx, message):
    logger.error(message)
    click.echo(ctx.get_help())
    sys.exit(1)


# Despite using setuptools to provide entry point, retain option for someone
# to also execute this script directly, for convenience.
if __name__ == "__main__":
    cli()
