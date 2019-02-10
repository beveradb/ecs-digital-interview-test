# SQL Migrations Runner
Python script to run SQL migration scripts sequentially from the specified folder,
updating latest schema version in the database itself in a table named "versionCode".

**Note**: this implementation exists purely as a solution for the ECS Digital technical test.

It almost certainly should **not** be used for any real-world use case, as mature solutions
exist for almost every use case. See "Problem Overview" section of NOTES for further
commentary on this topic. 

------------------------

## Installation

Install the `run_migrations` script with [pip](https://packaging.python.org/tutorials/installing-packages/).

```sh
$ pip install run_migrations
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
