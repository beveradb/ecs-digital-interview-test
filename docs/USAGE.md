Usage
=====

## Requirements

* Python 2.7, or 3.5+
* Existing MySQL or MariaDB database, either running locally or on a remote host.
* Table called `versionTable`, with a single `int(11)` column named "version". See [here](https://github.com/beveradb/migration_runner/blob/master/sql-migrations/001.create_migrations_version_table.sql) for schema.
* Directory containing SQL scripts to execute to migrate the database to each version.
   * Each migration / version should have one file.
   * Files should be named to match the pattern `VERSION.brief_description.sql`,
     where VERSION is an integer representing the database version after executing that script.
* Version numbers should be unique and sequential for consistent results.

## Basic usage

Run all SQL scripts in the specified directory, skipping any with a version number 
(numeric filename prefix) lower than the existing version stored in `versionTable`:
```
$ migration_runner ./folder-of-sql-scripts db_user db_hostname db_name db_password
```

## Options

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

##### Successful usage:
```
$ migration_runner sql-migrations test_user beveradb.tk test_db test_password

2019-02-12 13:37:29 - info: Starting with database version: 0
2019-02-12 13:37:29 - info: Migrations yet to be processed: 10 (out of 11 in dir)
2019-02-12 13:37:29 - info: Upgraded DB version from 0 to 1 by executing file: 'sql-migrations/001.create_migrations_version_table.sql'
2019-02-12 13:37:30 - info: Upgraded DB version from 0 to 2 by executing file: 'sql-migrations/2.set_current_version_to_1.sql'
2019-02-12 13:37:31 - info: Upgraded DB version from 2 to 45 by executing file: 'sql-migrations/045.createtable.sql'
2019-02-12 13:37:31 - info: Upgraded DB version from 45 to 46 by executing file: 'sql-migrations/046.create_seed_items.sql'
2019-02-12 13:37:32 - info: Upgraded DB version from 46 to 48 by executing file: 'sql-migrations/048.create_rooms.sql'
2019-02-12 13:37:33 - info: Upgraded DB version from 48 to 49 by executing file: 'sql-migrations/049 .rename-object-item.sql'
2019-02-12 13:37:34 - info: Upgraded DB version from 49 to 51 by executing file: 'sql-migrations/051-add-room-relations.sql'
2019-02-12 13:37:35 - info: Upgraded DB version from 51 to 52 by executing file: 'sql-migrations/052.create_customer_order.sql'
2019-02-12 13:37:36 - info: Upgraded DB version from 52 to 54 by executing file: 'sql-migrations/54-fix-customer-address-defaults.sql'
2019-02-12 13:37:37 - info: Upgraded DB version from 54 to 55 by executing file: 'sql-migrations/55exampleorder.sql'
2019-02-12 13:37:37 - info: Database version now 55 after processing 10 migrations. Remaining: 0.
```

##### Nothing to process:
```
$ migration_runner sql-migrations test_user beveradb.tk test_db test_password

2019-02-10 22:19:23 - info: Starting with database version: 55
2019-02-10 22:19:23 - info: Migrations yet to be processed: 0 (out of 11 in dir)
2019-02-10 22:19:23 - info: Database version now 55 after processing 0 migrations. Remaining: 0.
```

##### Missing argument:
```
$ migration_runner sql-migrations test_user beveradb.tk test_db

Usage: migration_runner [OPTIONS] SQL_DIRECTORY DB_USER DB_HOST DB_NAME
                      DB_PASSWORD
Try "migration_runner --help" for help.

Error: Missing argument "DB_PASSWORD".
```

##### Debug output:
```
$ migration_runner -l DEBUG sql-migrations test_user beveradb.tk test_db test_password

2019-02-10 22:21:48 - debug: CLI execution start
2019-02-10 22:21:48 - debug: Migrations found: 11
2019-02-10 22:21:48 - debug: Connecting to database with details: user=test_user, password=fake_password, host=beveradb.tk, db=migration_runner_test
2019-02-10 22:20:37 - error: Database connection error: 1045 (28000): Access denied for user 'test_user' (using password: YES)
```
