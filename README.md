SQL Migration Runner
======================

[//]: # (Latest PyPi Release)
[//]: # (Supported Python Versions)
[//]: # (Build Status)
[//]: # (Documentation Status)
[//]: # (Code Coverage)
[//]: # (Has Wheel Package)
[//]: # (Updates)

[![](https://img.shields.io/pypi/v/migration_runner.svg)](https://pypi.python.org/pypi/migration_runner)
[![](https://img.shields.io/pypi/pyversions/migration_runner.svg?style=flat)](https://pypi.python.org/pypi/migration_runner)
[![](https://img.shields.io/travis/beveradb/migration_runner.svg)](https://travis-ci.org/beveradb/migration_runner)
[![](https://readthedocs.org/projects/migration_runner/badge/?version=latest)](https://migration_runner.readthedocs.io/en/latest/?badge=latest)
[![](https://coveralls.io/repos/github/beveradb/migration_runner/badge.svg?branch=master)](https://coveralls.io/github/beveradb/migration_runner?branch=master)
[![](https://img.shields.io/pypi/wheel/migration_runner.svg)](https://pypi.org/project/migration_runner/#files)
[![](https://pyup.io/repos/github/beveradb/migration_runner/shield.svg)](https://pyup.io/repos/github/beveradb/migration_runner/)

Python script to run SQL migration scripts sequentially from the specified folder,
updating latest schema version in the database itself after each migration.

**WARNING**: this tool was created purely as a solution for the ECS Digital technical test.
See [PROBLEM](https://github.com/beveradb/migration_runner/blob/master/docs/PROBLEM.md) 
for details of the use case and requirements for the task.

It almost certainly should **not** be used for any real-world use case, as mature solutions
exist for almost every use case. See "Problem Overview" section of [NOTES](https://github.com/beveradb/migration_runner/blob/master/docs/NOTES.md) 
for further commentary on this topic. 

------------------------

## Requirements

* Python 2.7, or 3.5+
* Existing MySQL or MariaDB database, either running locally or on a remote host.
* Table called `versionTable`, with a single `int(11)` column named "version". See [here](https://github.com/beveradb/migration_runner/blob/master/sql-migrations/001.create_migrations_version_table.sql) for schema.
* Directory containing SQL scripts to execute to migrate the database to each version.
   * Each migration / version should have one file.
   * Files should be named to match the pattern `VERSION.brief_description.sql`,
     where VERSION is an integer representing the database version after executing that script.
* Version numbers should be unique and sequential for consistent results.

## Installation

To install Migration Runner, run this command in your terminal:

``` console
$ pip install migration_runner
```

This is the preferred method to install Migration Runner, as it will
always install the most recent stable release.

If you don't have [pip](https://pip.pypa.io) installed, this [Python
installation
guide](http://docs.python-guide.org/en/latest/starting/installation/)
can guide you through the process.

For instructions on building from source, see the 
[documentation](https://migration_runner.readthedocs.io).

## Usage

Run the `migration_runner` script with `--help` to get usage instructions:

```
$ migration_runner --help

Usage: migration_runner [OPTIONS] SQL_DIRECTORY DB_USER DB_HOST DB_NAME DB_PASSWORD

  A cli tool for executing SQL migrations in sequence.

Options:
  -s, --single-file TEXT  Filename of single SQL script to process.
  -l, --loglevel LVL      Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  -v, --version           Show the version and exit.
  --help                  Show this message and exit.
```

## Examples

#### Successful usage:
```
$ migration_runner sql-migrations beveradb migration_runner_test.beveradb.tk test_user test_password

2019-02-10 22:16:30,394 - info: Starting with database version: 0
2019-02-10 22:16:30,395 - info: Migrations yet to be processed: 10 (out of 11 in dir)
2019-02-10 22:16:30,721 - info: Successfully upgraded database from version: 0 to 1 by executing migration in file: 'sql-migrations/001.create_migrations_version_table.sql'
2019-02-10 22:16:31,566 - info: Successfully upgraded database from version: 1 to 2 by executing migration in file: 'sql-migrations/2.set_current_version_to_1.sql'
2019-02-10 22:16:32,562 - info: Successfully upgraded database from version: 2 to 45 by executing migration in file: 'sql-migrations/045.createtable.sql'
2019-02-10 22:16:33,236 - info: Successfully upgraded database from version: 45 to 46 by executing migration in file: 'sql-migrations/046.create_seed_items.sql'
2019-02-10 22:16:34,173 - info: Successfully upgraded database from version: 46 to 48 by executing migration in file: 'sql-migrations/048.create_rooms.sql'
2019-02-10 22:16:34,849 - info: Successfully upgraded database from version: 48 to 49 by executing migration in file: 'sql-migrations/049 .rename-object-item.sql'
2019-02-10 22:16:36,258 - info: Successfully upgraded database from version: 49 to 51 by executing migration in file: 'sql-migrations/051-add-room-relations.sql'
2019-02-10 22:16:37,165 - info: Successfully upgraded database from version: 51 to 52 by executing migration in file: 'sql-migrations/052.create_customer_order.sql'
2019-02-10 22:16:38,299 - info: Successfully upgraded database from version: 52 to 54 by executing migration in file: 'sql-migrations/54-fix-customer-address-defaults.sql'
2019-02-10 22:16:39,150 - info: Successfully upgraded database from version: 54 to 55 by executing migration in file: 'sql-migrations/55exampleorder.sql'
2019-02-10 22:16:39,499 - info: Database version now 55 after processing 10 migrations. Remaining: 0.
```

#### Nothing to process:
```
$ migration_runner sql-migrations test_user beveradb.tk migration_runner_test test_password

2019-02-10 22:19:23,252 - info: Starting with database version: 55
2019-02-10 22:19:23,252 - info: Migrations yet to be processed: 0 (out of 11 in dir)
2019-02-10 22:19:23,252 - info: Database version now 55 after processing 0 migrations. Remaining: 0.
```

#### Missing argument:
```
$ migration_runner sql-migrations test_user beveradb.tk migration_runner_test

Usage: migration_runner [OPTIONS] SQL_DIRECTORY DB_USER DB_HOST DB_NAME
                      DB_PASSWORD
Try "migration_runner --help" for help.

Error: Missing argument "DB_PASSWORD".
```

#### Debug output:
```
$ migration_runner -l DEBUG sql-migrations test_user beveradb.tk migration_runner_test fake_password

2019-02-10 22:21:48,074 - debug: CLI execution start
2019-02-10 22:21:48,075 - debug: Migrations found: 11
2019-02-10 22:21:48,075 - debug: Connecting to database with details: user=test_user, password=fake_password, host=beveradb.tk, db=migration_runner_test
2019-02-10 22:20:37,731 - error: Database connection error: 1045 (28000): Access denied for user 'test_user' (using password: YES)
```
