import pytest
from mock import call

import run_migrations as r


def test_extract_sequence_sql_filename_expected(sql_filename_expected):
    version = r.extract_sequence_num(sql_filename_expected)
    assert version == 45


def test_extract_sequence_sql_filename_hyphen(sql_filename_hyphen):
    version = r.extract_sequence_num(sql_filename_hyphen)
    assert version == 45


def test_extract_sequence_sql_filename_not_zero_padded(
        sql_filename_not_zero_padded):
    version = r.extract_sequence_num(sql_filename_not_zero_padded)
    assert version == 45


def test_extract_sequence_sql_filename_spaced(sql_filename_spaced):
    version = r.extract_sequence_num(sql_filename_spaced)
    assert version == 45


def test_extract_sequence_sql_filename_no_sql_suffix(
        sql_filename_no_sql_suffix):
    version = r.extract_sequence_num(sql_filename_no_sql_suffix)
    assert version == 45


def test_extract_sequence_sql_filename_no_separator(
        sql_filename_no_separator):
    version = r.extract_sequence_num(sql_filename_no_separator)
    assert version == 45


def test_extract_sequence_sql_filename_bigint(
        sql_filename_bigint):
    version = r.extract_sequence_num(sql_filename_bigint)
    assert version == 23514352834592347502351435283459234750


def test_extract_sequence_sql_filename_no_version(
        sql_filename_no_version):
    with pytest.raises(AttributeError):
        r.extract_sequence_num(sql_filename_no_version)


def test_append_migration_sql_filename_expected(sql_filename_expected):
    migrations = []
    r.append_migration(migrations, sql_filename_expected)
    assert migrations == [(45, sql_filename_expected)]


def test_append_migration_sql_filename_expected_existing_value(
        sql_filename_expected):
    migrations = [(2, "test.sql")]
    r.append_migration(migrations, sql_filename_expected)
    assert migrations == [(2, "test.sql"),
                          (45, sql_filename_expected)]


def test_find_migrations_expected(tmpdir, sql_filename_expected):
    filepath = tmpdir.join(sql_filename_expected)
    filepath.write("test")
    migrations = r.find_migrations(str(tmpdir))
    assert migrations == [(45, str(filepath))]


def test_find_migrations_empty(tmpdir):
    migrations = r.find_migrations(str(tmpdir))
    assert migrations == []


def test_find_migrations_no_suffix(tmpdir, sql_filename_no_sql_suffix):
    filepath = tmpdir.join(sql_filename_no_sql_suffix)
    filepath.write("test")
    migrations = r.find_migrations(str(tmpdir))
    assert migrations == []


def test_find_migrations_multiple(
        tmpdir,
        sql_filename_expected,
        sql_filename_bigint,
        sql_filename_no_sql_suffix,
        sql_filename_spaced
):
    sql_filename_expected_filepath = tmpdir.join(sql_filename_expected)
    sql_filename_expected_filepath.write("test")

    sql_filename_bigint_filepath = tmpdir.join(sql_filename_bigint)
    sql_filename_bigint_filepath.write("test")

    sql_filename_no_sql_suffix_path = tmpdir.join(sql_filename_no_sql_suffix)
    sql_filename_no_sql_suffix_path.write("test")

    sql_filename_spaced_path = tmpdir.join(sql_filename_spaced)
    sql_filename_spaced_path.write("test")

    migrations = r.find_migrations(str(tmpdir))
    assert migrations == [
        (45, str(sql_filename_expected_filepath)),
        (23514352834592347502351435283459234750,
         str(sql_filename_bigint_filepath)),
        (45, str(sql_filename_spaced_path))
    ]


def test_sort_migrations_expected(unsorted_migrations_tuple_list):
    r.sort_migrations(unsorted_migrations_tuple_list)
    assert unsorted_migrations_tuple_list == [
        (1, '/tmp/001.createtable.sql'),
        (2, '/tmp/2-createtable.sql'),
        (45, '/tmp/045.createtable.sql'),
        (60, '/tmp/60.createtable.sql'),
    ]


def test_sort_migrations_not_tuples(unsorted_migrations_string_list):
    with pytest.raises(TypeError):
        r.sort_migrations(unsorted_migrations_string_list)


def test_sort_migrations_not_versioned_tuples(
        unsorted_migrations_non_versioned_list):
    with pytest.raises(TypeError):
        r.sort_migrations(unsorted_migrations_non_versioned_list)


def test_populate_migrations_calls_find_migrations(mocker, tmpdir):
    mocker.patch('run_migrations.find_migrations')

    r.populate_migrations(str(tmpdir))

    r.find_migrations.assert_called_with(str(tmpdir))


def test_populate_migrations_calls_sort_migrations(mocker,
                                                   tmpdir,
                                                   sql_filename_expected):
    sql_filename_expected_filepath = tmpdir.join(sql_filename_expected)
    sql_filename_expected_filepath.write("test")

    mocker.patch('run_migrations.sort_migrations')

    r.populate_migrations(str(tmpdir))

    r.sort_migrations.assert_called_with(
        [(45, sql_filename_expected_filepath)]
    )


def test_connect_database_invalid_params(db_params_tup):
    with pytest.raises(SystemExit):
        r.connect_database(db_params_tup)


def test_connect_database_mysql_library_called(mocker, db_params_tup,
                                               db_params_dict):
    mocker.patch('run_migrations.mysql.connector.connect')
    r.connect_database(db_params_tup)

    r.mysql.connector.connect.assert_called_with(**db_params_dict)


def test_fetch_current_version_calls_connect(mocker, db_params_tup,
                                             db_params_dict):
    mocker.patch('run_migrations.mysql.connector.connect')
    r.fetch_current_version(db_params_tup)

    r.mysql.connector.connect.assert_called_with(**db_params_dict)


def test_fetch_current_version_fetches_expected_value(mocker, db_params_tup):
    expected = 45
    mocker.patch('run_migrations.mysql.connector.connect')

    mock_connection = r.mysql.connector.connect.return_value
    mock_cursor = mock_connection.cursor.return_value
    mock_cursor.fetchone.return_value = (expected,)

    result = r.fetch_current_version(db_params_tup)

    assert result == expected


def test_fetch_current_version_invalid_db_params(db_params_tup):
    with pytest.raises(SystemExit):
        r.fetch_current_version(db_params_tup)


def test_fetch_current_version_no_version_in_database(mocker, db_params_tup):
    mocker.patch('run_migrations.mysql.connector.connect')

    mock_connection = r.mysql.connector.connect.return_value
    mock_cursor = mock_connection.cursor.return_value

    mock_cursor.fetchone.side_effect = \
        r.mysql.connector.errors.ProgrammingError(
            "1146 (42S02): Table 'versionTable' doesn't exist")

    result = r.fetch_current_version(db_params_tup)

    assert result == 0


def test_get_unprocessed_migrations_version_0(unsorted_migrations_tuple_list):
    result = r.get_unprocessed_migrations(0, unsorted_migrations_tuple_list)
    assert result == unsorted_migrations_tuple_list


def test_get_unprocessed_migrations_version_10(unsorted_migrations_tuple_list):
    expected = [
        (45, '/tmp/045.createtable.sql'),
        (60, '/tmp/60.createtable.sql'),
    ]

    result = r.get_unprocessed_migrations(10, unsorted_migrations_tuple_list)

    assert result == expected


def test_get_unprocessed_migrations_version_59(unsorted_migrations_tuple_list):
    expected = [
        (60, '/tmp/60.createtable.sql'),
    ]
    result = r.get_unprocessed_migrations(59, unsorted_migrations_tuple_list)

    assert result == expected


def test_get_unprocessed_migrations_version_60(unsorted_migrations_tuple_list):
    expected = []
    result = r.get_unprocessed_migrations(60, unsorted_migrations_tuple_list)

    assert result == expected


def test_get_unprocessed_migrations_version_61(unsorted_migrations_tuple_list):
    expected = []
    result = r.get_unprocessed_migrations(61, unsorted_migrations_tuple_list)

    assert result == expected


def test_get_unprocessed_migrations_version_string(
        unsorted_migrations_tuple_list):
    expected = []

    result = r.get_unprocessed_migrations(
        'five',
        unsorted_migrations_tuple_list)

    assert result == expected


def test_apply_migration_expected_opens_file(tmpdir, mocker, db_params_tup,
                                             sql_filename_expected):
    mocker.patch('run_migrations.mysql.connector.connect')
    mocker.patch('run_migrations.open')

    filepath = tmpdir.join(sql_filename_expected)
    filepath.write("test")

    r.apply_migration(db_params_tup, str(filepath))

    r.open.assert_called_with(str(filepath))


def test_apply_migration_expected_calls_connect(tmpdir, mocker, db_params_tup,
                                                db_params_dict,
                                                sql_filename_expected):
    mocker.patch('run_migrations.mysql.connector.connect')

    filepath = tmpdir.join(sql_filename_expected)
    filepath.write("test")

    r.apply_migration(db_params_tup, str(filepath))

    r.mysql.connector.connect.assert_called_with(**db_params_dict)


def test_apply_migration_expected_executes_file(tmpdir, mocker, db_params_tup,
                                                sql_filename_expected):
    mocker.patch('run_migrations.mysql.connector.connect')

    filepath = tmpdir.join(sql_filename_expected)
    filepath.write("test")

    mock_connection = r.mysql.connector.connect.return_value
    mock_cursor = mock_connection.cursor.return_value

    r.apply_migration(db_params_tup, str(filepath))

    mock_cursor.execute.assert_called_with("test", multi=True)


def test_process_single_file_calls_apply(mocker, db_params_tup,
                                         sql_filename_expected):
    mocker.patch('run_migrations.apply_migration')
    r.process_single_file(db_params_tup, sql_filename_expected)
    r.apply_migration.assert_called_with(db_params_tup, sql_filename_expected)


def test_update_current_version_calls_connect(mocker, db_params_tup,
                                              db_params_dict):
    mocker.patch('run_migrations.mysql.connector.connect')

    r.update_current_version(db_params_tup, 45)

    r.mysql.connector.connect.assert_called_with(**db_params_dict)


def test_update_current_version_executes_update(mocker, db_params_tup):
    mocker.patch('run_migrations.mysql.connector.connect')

    mock_connection = r.mysql.connector.connect.return_value
    mock_cursor = mock_connection.cursor.return_value

    r.update_current_version(db_params_tup, 45)

    mock_cursor.execute.assert_has_calls([
        call("UPDATE versionTable SET version = \'45\'"),
        call("SELECT version FROM versionTable LIMIT 1"),
    ])


def test_update_current_version_returns_new_version(mocker, db_params_tup):
    mocker.patch('run_migrations.mysql.connector.connect')

    expected = 45

    mock_connection = r.mysql.connector.connect.return_value
    mock_cursor = mock_connection.cursor.return_value
    mock_cursor.fetchone.return_value = (expected,)

    result = r.update_current_version(db_params_tup, expected)

    assert result == expected


def test_update_current_version_returns_0_if_version_invalid(mocker,
                                                             db_params_tup):
    mocker.patch('run_migrations.mysql.connector.connect')

    mock_connection = r.mysql.connector.connect.return_value
    mock_cursor = mock_connection.cursor.return_value

    mock_cursor.execute.side_effect = \
        r.mysql.connector.errors.DataError(
            "1366 (22007): Incorrect integer value: 'five' for column"
            " `versionTable`.`version` at row 1")

    result = r.update_current_version(db_params_tup, 'five')

    assert result == 0


def test_process_migrations_calls_apply(mocker, db_params_tup,
                                        sorted_migrations_tuple_list):
    mocker.patch('run_migrations.apply_migration')
    mocker.patch('run_migrations.update_current_version')

    r.process_migrations(db_params_tup, 0, sorted_migrations_tuple_list)

    r.apply_migration.assert_has_calls([
        call(db_params_tup, '/tmp/001.createtable.sql'),
        call(db_params_tup, '/tmp/2-createtable.sql'),
        call(db_params_tup, '/tmp/045.createtable.sql'),
        call(db_params_tup, '/tmp/60.createtable.sql'),
    ])


def test_process_migrations_calls_update(mocker, db_params_tup,
                                         sorted_migrations_tuple_list):
    mocker.patch('run_migrations.apply_migration')
    mocker.patch('run_migrations.update_current_version')

    r.process_migrations(db_params_tup, 0, sorted_migrations_tuple_list)

    r.update_current_version.assert_has_calls([
        call(db_params_tup, 1),
        call(db_params_tup, 2),
        call(db_params_tup, 45),
        call(db_params_tup, 60)
    ], any_order=True)


def test_process_migrations_returns_expected(mocker, db_params_tup,
                                             sorted_migrations_tuple_list):
    mocker.patch('run_migrations.apply_migration')
    mocker.patch('run_migrations.update_current_version')

    r.update_current_version.return_value = 60

    db_version, total_processed = r.process_migrations(
        db_params_tup, 0, sorted_migrations_tuple_list)

    assert db_version == 60
    assert total_processed == 4
