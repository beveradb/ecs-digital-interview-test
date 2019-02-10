# SQL Migrations Runner

![Supported Python Versions: 2.7, 3.5, 3.6, 3.7](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7-blue.svg)

Python script to run SQL migration scripts sequentially from the specified folder,
updating latest schema version in the database itself after each migration.

**WARNING**: this implementation exists purely as a solution for the ECS Digital technical test.
See [PROBLEM](https://github.com/beveradb/python-sql-migration-runner/blob/master/PROBLEM.md) 
for details of the use case and requirements for the task.

It almost certainly should **not** be used for any real-world use case, as mature solutions
exist for almost every use case. See "Problem Overview" section of [NOTES](https://github.com/beveradb/python-sql-migration-runner/blob/master/NOTES.md) 
for further commentary on this topic. 

------------------------

## Requirements

* Python 2.7, or 3.5+
* Existing MySQL or MariaDB database, either running locally or on a remote host.
* Table called `versionTable`, with a single `int(11)` column named "version". See [here](https://github.com/beveradb/python-sql-migration-runner/blob/master/sql-migrations/001.create_migrations_version_table.sql) for schema.
* Directory containing SQL scripts to execute to migrate the database to each version.
   * Each migration / version should have one file.
   * Files should be named to match the pattern `VERSION.brief_description.sql`,
     where VERSION is an integer representing the database version after executing that script.
* Version numbers should be unique and sequential for consistent results.

## Installation

Install the `run_migrations` script with [pip](https://packaging.python.org/tutorials/installing-packages/).

```sh
$ pip install git+git://github.com/beveradb/python-sql-migration-runner.git
```

## Usage

Run the `run_migrations` script with `--help` to get usage instructions:

```
$ run_migrations --help

Usage: run_migrations [OPTIONS] SQL_DIRECTORY DB_USER DB_HOST DB_NAME DB_PASSWORD

  A cli tool for executing SQL migrations in sequence.

Options:
  -s, --single-file TEXT  Filename of single SQL script to process.
  -l, --loglevel LVL      Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  -v, --version           Show the version and exit.
  --help                  Show this message and exit.
```
